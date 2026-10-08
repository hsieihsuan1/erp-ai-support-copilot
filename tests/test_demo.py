import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.retrieval import chunk_text


@pytest.fixture
def client():
    return TestClient(create_app())


def ask(client, who='alpha-agent', **kwargs):
    return client.post('/api/chat',headers={'X-Demo-Identity':who},json={'message':'DEMO-AP-001 invoice validation','module':'Payables',**kwargs})


def test_health_no_remote(client):
    assert client.get('/health').json()['remote_calls'] is False


@pytest.mark.parametrize('who',['','unknown'])
def test_identity_required(client,who):
    assert ask(client,who).status_code == 401


def test_tenant_filter(client):
    alpha=ask(client).json(); beta=ask(client,'beta-agent').json()
    assert [s['id'] for s in alpha['sources']] == ['alpha-ap-001']
    assert [s['id'] for s in beta['sources']] == ['beta-ap-001']
    assert 'beta review queue' not in alpha['message']
    assert 'beta review queue' in beta['message']


@pytest.mark.parametrize('other',['beta-agent','alpha-reviewer'])
def test_session_owner_isolation(client,other):
    sid=ask(client).json()['session_id']
    headers={'X-Demo-Identity':other}
    assert client.get('/api/session/'+sid,headers=headers).status_code==404
    assert ask(client,other,session_id=sid).status_code==404
    assert client.post('/api/tickets',headers=headers,json={'session_id':sid,'confirmed':True}).status_code==404


def test_cannot_supply_tenant_or_confidence(client):
    assert ask(client,tenant='beta').status_code == 422
    assert ask(client,confidence=1).status_code == 422


def test_no_evidence_suggests_escalation(client):
    result=ask(client,message='zyxnonexistent').json()
    assert result['sources']==[] and result['needs_ticket'] and not result['resolved']
    assert 'confidence' not in result


def test_module_filter(client):
    assert ask(client,module='Other').json()['sources']==[]


def test_three_unverified_turns(client):
    first=ask(client).json();sid=first['session_id']
    second=ask(client,session_id=sid).json();third=ask(client,session_id=sid).json()
    assert not first['needs_ticket'] and not second['needs_ticket']
    assert third['needs_ticket'] and third['turn_count']==3


@pytest.mark.parametrize('provider',['servicenow','jira'])
def test_ticket_confirmation_and_idempotence(client,provider):
    sid=ask(client).json()['session_id'];headers={'X-Demo-Identity':'alpha-agent'}
    data={'session_id':sid,'provider':provider}
    assert client.post('/api/tickets',headers=headers,json=data).status_code==409
    data['confirmed']=True
    first=client.post('/api/tickets',headers=headers,json=data).json()
    second=client.post('/api/tickets',headers=headers,json=data).json()
    assert first==second and first['mode']=='mock' and first['id'].startswith('MOCK-')
    assert len(first['transcript'])==2


def test_unknown_session(client):
    assert ask(client,session_id='not-a-session').status_code==404


@pytest.mark.parametrize('message',['','   ','x'*2001])
def test_message_bounds(client,message):
    assert ask(client,message=message).status_code==422


def test_chunker_terminates_and_bounds():
    assert chunk_text('')==[]
    assert chunk_text('small')==['small']
    text='word '*600
    chunks=chunk_text(text,size=100,overlap=20)
    assert len(chunks)<100 and all(len(c)<=100 for c in chunks)
    assert chunks[-1].endswith('word')
    with pytest.raises(ValueError):chunk_text('text',100,100)


def test_host_pages(client):
    for path in ['/', '/demo/erp', '/widget/widget.html']:
        assert client.get(path).status_code==200
