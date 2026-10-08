/**
 * erp-patterns.js
 * URL-to-module/page mapping for supported ERP platforms.
 *
 * Each platform entry contains an ordered list of pattern matchers.
 * Patterns are evaluated top-to-bottom; the first match wins.
 *
 * Structure:
 *   ERP_PATTERNS[platform] = [
 *     { test: RegExp, module: string, page: string }
 *   ]
 *
 * Consumed by content/inject.js via window.ERP_PATTERNS.
 */

/* global window */

window.ERP_PATTERNS = {

  // ─────────────────────────────────────────────────────────────────
  // Oracle Fusion Cloud
  // Hostnames: *.oracle.com, *.oraclecloud.com
  // Base UI path: /fscmUI/faces/  (Oracle Fusion Applications UI)
  // ─────────────────────────────────────────────────────────────────
  oracle_fusion: [
    // ── Home / Dashboard ──────────────────────────────────────────
    { test: /\/fscmUI\/faces\/FuseWelcome/i,              module: 'Home',             page: 'Dashboard' },
    { test: /\/fscmUI\/faces\/FuseOverview/i,             module: 'Home',             page: 'Overview' },

    // ── Financials - Payables ─────────────────────────────────────
    { test: /\/payables\/.*[Cc]reate[Ii]nvoice/,          module: 'Payables',         page: 'CreateInvoice' },
    { test: /\/payables\/.*[Ii]nvoice/,                   module: 'Payables',         page: 'Invoices' },
    { test: /\/payables\/.*[Pp]ayment/,                   module: 'Payables',         page: 'Payments' },
    { test: /\/payables\//,                               module: 'Payables',         page: 'Overview' },

    // ── Financials - Receivables ──────────────────────────────────
    { test: /\/receivables\/.*[Ii]nvoice/,                module: 'Receivables',      page: 'Invoices' },
    { test: /\/receivables\/.*[Rr]eceipt/,                module: 'Receivables',      page: 'Receipts' },
    { test: /\/receivables\/.*[Cc]ustomer/,               module: 'Receivables',      page: 'Customers' },
    { test: /\/receivables\//,                            module: 'Receivables',      page: 'Overview' },

    // ── Financials - General Ledger ───────────────────────────────
    { test: /\/generalLedger\/.*[Jj]ournal/,              module: 'General Ledger',   page: 'Journals' },
    { test: /\/generalLedger\/.*[Bb]udget/,               module: 'General Ledger',   page: 'Budgets' },
    { test: /\/generalLedger\//,                          module: 'General Ledger',   page: 'Overview' },

    // ── Financials - Expenses ─────────────────────────────────────
    { test: /\/expenses\/.*[Rr]eport/,                    module: 'Expenses',         page: 'ExpenseReport' },
    { test: /\/expenses\//,                               module: 'Expenses',         page: 'Overview' },

    // ── Financials - Assets ───────────────────────────────────────
    { test: /\/assetManagement\/.*[Aa]ddition/,           module: 'Fixed Assets',     page: 'AddAsset' },
    { test: /\/assetManagement\/.*[Rr]etirement/,         module: 'Fixed Assets',     page: 'RetireAsset' },
    { test: /\/assetManagement\//,                        module: 'Fixed Assets',     page: 'Overview' },

    // ── Procurement ───────────────────────────────────────────────
    { test: /\/procurement\/.*[Pp]urchase[Oo]rder/,       module: 'Procurement',      page: 'PurchaseOrder' },
    { test: /\/procurement\/.*[Rr]equisition/,            module: 'Procurement',      page: 'Requisition' },
    { test: /\/procurement\/.*[Ss]upplier/,               module: 'Procurement',      page: 'Suppliers' },
    { test: /\/procurement\//,                            module: 'Procurement',      page: 'Overview' },

    // ── Supply Chain - Inventory ──────────────────────────────────
    { test: /\/inventory\/.*[Tt]ransaction/,              module: 'Inventory',        page: 'Transactions' },
    { test: /\/inventory\/.*[Ii]tem/,                     module: 'Inventory',        page: 'Items' },
    { test: /\/inventory\//,                              module: 'Inventory',        page: 'Overview' },

    // ── Supply Chain - Order Management ──────────────────────────
    { test: /\/orderManagement\/.*[Ss]ales[Oo]rder/,      module: 'OrderManagement',  page: 'SalesOrder' },
    { test: /\/orderManagement\//,                        module: 'OrderManagement',  page: 'Overview' },

    // ── HCM - Human Resources ─────────────────────────────────────
    { test: /\/hcmUI\/.*[Ee]mployee/,                     module: 'HCM',              page: 'Employees' },
    { test: /\/hcmUI\/.*[Hh]ire/,                         module: 'HCM',              page: 'HireEmployee' },
    { test: /\/hcmUI\/.*[Pp]ayroll/,                      module: 'HCM',              page: 'Payroll' },
    { test: /\/hcmUI\/.*[Aa]bsence/,                      module: 'HCM',              page: 'Absences' },
    { test: /\/hcmUI\//,                                  module: 'HCM',              page: 'Overview' },

    // ── Projects ──────────────────────────────────────────────────
    { test: /\/projectsControl\/.*[Tt]ask/,               module: 'Projects',         page: 'Tasks' },
    { test: /\/projectsControl\//,                        module: 'Projects',         page: 'Overview' },

    // ── CX / CRM ──────────────────────────────────────────────────
    { test: /\/crmUI\/.*[Oo]pportunity/,                  module: 'CRM',              page: 'Opportunities' },
    { test: /\/crmUI\/.*[Cc]ontact/,                      module: 'CRM',              page: 'Contacts' },
    { test: /\/crmUI\//,                                  module: 'CRM',              page: 'Overview' },

    // ── Catch-all for Oracle Fusion hosts ─────────────────────────
    { test: /\/fscmUI\//,                                 module: 'OracleFusion',     page: 'Unknown' }
  ],

  // ─────────────────────────────────────────────────────────────────
  // SAP (generic patterns covering SAP S/4HANA Cloud, SAP Fiori)
  // Hostnames: *.sap.com, internal SAP landscapes
  // ─────────────────────────────────────────────────────────────────
  sap: [
    // SAP Fiori Launchpad
    { test: /\/ui#[Ss]hell-home/,                         module: 'SAP',              page: 'FioriLaunchpad' },
    { test: /\/ui#/,                                      module: 'SAP',              page: 'FioriApp' },

    // S/4HANA - Finance
    { test: /\/sap\/bc\/.*F0707/i,                        module: 'SAP_Finance',      page: 'PostJournalEntry' },
    { test: /\/sap\/bc\/.*F1076/i,                        module: 'SAP_Finance',      page: 'ManageJournalEntries' },
    { test: /\/sap\/bc\/.*AP/i,                           module: 'SAP_Payables',     page: 'Overview' },
    { test: /\/sap\/bc\/.*AR/i,                           module: 'SAP_Receivables',  page: 'Overview' },

    // Generic SAP WebDynpro / ABAP
    { test: /\/sap\/bc\/webdynpro\//i,                    module: 'SAP',              page: 'WebDynpro' },
    { test: /\/sap\/bc\/bsp\//i,                          module: 'SAP',              page: 'BSP' },
    { test: /\/sap\//,                                    module: 'SAP',              page: 'Unknown' }
  ],

  // ─────────────────────────────────────────────────────────────────
  // Workday
  // Hostnames: *.workday.com
  // ─────────────────────────────────────────────────────────────────
  workday: [
    // HCM
    { test: /\/d\/task\/.*hire/i,                         module: 'Workday_HCM',      page: 'HireWorker' },
    { test: /\/d\/task\/.*termination/i,                  module: 'Workday_HCM',      page: 'TerminateWorker' },
    { test: /\/d\/task\/.*job/i,                          module: 'Workday_HCM',      page: 'JobChange' },

    // Payroll
    { test: /\/d\/task\/.*payroll/i,                      module: 'Workday_Payroll',  page: 'Overview' },
    { test: /\/d\/task\/.*payslip/i,                      module: 'Workday_Payroll',  page: 'Payslip' },

    // Finance
    { test: /\/d\/task\/.*journal/i,                      module: 'Workday_Finance',  page: 'Journal' },
    { test: /\/d\/task\/.*expense/i,                      module: 'Workday_Finance',  page: 'Expenses' },
    { test: /\/d\/task\/.*supplier/i,                     module: 'Workday_Finance',  page: 'Suppliers' },
    { test: /\/d\/task\/.*invoice/i,                      module: 'Workday_Finance',  page: 'Invoices' },

    // Recruiting
    { test: /\/d\/task\/.*recruit/i,                      module: 'Workday_Recruiting', page: 'Overview' },
    { test: /\/d\/task\/.*requisition/i,                  module: 'Workday_Recruiting', page: 'JobRequisition' },

    // Generic Workday task/report
    { test: /\/d\/task\//,                                module: 'Workday',          page: 'Task' },
    { test: /\/d\/report\//,                              module: 'Workday',          page: 'Report' },
    { test: /\/wday\//,                                   module: 'Workday',          page: 'Unknown' }
  ]
};

/**
 * Detect which ERP platform the current URL belongs to.
 * Returns { platform, patterns } or null when no platform matches.
 *
 * @param {string} url
 * @returns {{ platform: string, patterns: Array }|null}
 */
window.detectERPPlatform = function detectERPPlatform(url) {
  let parsed;
  try { parsed = new URL(url); } catch { return null; }
  if (!['http:', 'https:'].includes(parsed.protocol)) return null;
  const host = parsed.hostname.toLowerCase();
  const belongs = domain => host === domain || host.endsWith('.' + domain);
  if (belongs('oracle.com') || belongs('oraclecloud.com'))
    return { platform: 'oracle_fusion', patterns: window.ERP_PATTERNS.oracle_fusion };
  if (belongs('sap.com')) return { platform: 'sap', patterns: window.ERP_PATTERNS.sap };
  if (belongs('workday.com')) return { platform: 'workday', patterns: window.ERP_PATTERNS.workday };
  return null;
};

/**
 * Resolve module and page for a given URL using the pattern tables.
 *
 * @param {string} url
 * @returns {{ platform: string, module: string, page: string }|null}
 */
window.resolveERPContext = function resolveERPContext(url) {
  const detected = window.detectERPPlatform(url);
  if (!detected) return null;

  const { platform, patterns } = detected;
  for (const entry of patterns) {
    if (entry.test.test(url)) {
      return { platform, module: entry.module, page: entry.page };
    }
  }
  // Platform matched but no specific page pattern found
  return { platform, module: platform, page: 'Unknown' };
};
