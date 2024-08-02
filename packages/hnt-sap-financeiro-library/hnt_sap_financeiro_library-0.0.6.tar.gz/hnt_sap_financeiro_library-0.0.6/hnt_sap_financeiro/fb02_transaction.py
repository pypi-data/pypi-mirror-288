import logging

from hnt_sap_financeiro.common.tx_result import TxResult
from hnt_sap_financeiro.hnt_sap_exception import HntSapException
from hnt_sap_financeiro.sap_status_bar import sbar_extracted_text
logger = logging.getLogger(__name__)

MSG_SAP_CODIGO_DOCUMENTO = "^Documento ([0-9]*) só foi pré-editado$"
MSG_SAP_ERROR_CODIGO_BARRAS = 'Grupo(s) dos nºs código de barras 1 2 3 errado(s)'
MSG_SAP_ALT_DA_FORMA_PAGAMENTO = 'Alt da Forma de Pagamento "I" ou "N" não permitido. Contactar financeiro'
MSG_SAP_NENHUMA_MODIFICACAO = 'Nenhuma modificação efetuada'
class Fb02Transaction:
    def __init__(self) -> None:
        pass

    def execute(self, sapGuiLib, codigo_contabil, bar_code):
        logger.info(f"Enter execute codigo_contabil:{codigo_contabil}, bar_code:{bar_code}")

        sapGuiLib.run_transaction('/nFB02')

        sapGuiLib.session.findById("wnd[0]/usr/txtRF05L-BELNR").Text = codigo_contabil # '[SAP: Nº documento | Doc contábil da FV60]
        sapGuiLib.session.findById("wnd[0]/usr/ctxtRF05L-BUKRS").Text = "HFNT"#  '[SAP: Empresa | Constante]
        sapGuiLib.session.findById("wnd[0]/usr/txtRF05L-GJAHR").Text = "2024"#  '[SAP: Exercício | Ano lçto do doc contábil]
        sapGuiLib.send_vkey(0)
        sbar = sapGuiLib.session.findById("wnd[0]/sbar").Text
        documento = sbar_extracted_text(MSG_SAP_CODIGO_DOCUMENTO, sbar)
        if documento == codigo_contabil:
            raise HntSapException(sbar)
        # 'Filtro D/C
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").setCurrentCell(-1, "SHKZG") 
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").selectColumn("SHKZG")
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").selectedRows = ""
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").pressToolbarButton("&MB_FILTER")
        sapGuiLib.session.findById("wnd[1]/usr/ssub%_SUBSCREEN_FREESEL:SAPLSSEL:1105/ctxt%%DYN001-LOW").Text = "H"
        sapGuiLib.session.findById("wnd[1]/tbar[0]/btn[0]").press()

        # 'Duplo clique linha "H"
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").currentCellColumn = "SHKZG"
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").selectedRows = "0"
        sapGuiLib.session.findById("wnd[0]/usr/cntlCTRL_CONTAINERBSEG/shellcont/shell").doubleClickCurrentCell()

        sapGuiLib.session.findById("wnd[0]/usr/txtRF05L-BRCDE").Text = bar_code # '[SAP: Refer.banco | JIRA: Código de Barras]

        sapGuiLib.session.findById("wnd[0]/tbar[0]/btn[11]").press()#  '[Salvar]
        sbar = sapGuiLib.session.findById("wnd[0]/sbar").Text
        if sbar == MSG_SAP_ERROR_CODIGO_BARRAS or sbar == MSG_SAP_ALT_DA_FORMA_PAGAMENTO or sbar == MSG_SAP_NENHUMA_MODIFICACAO:
            raise HntSapException(sbar)
        result = TxResult(codigo_contabil, sbar)
        logger.info(f"Leave execute taxa:{result}")
        return result