import asyncio
import re
import time
import warnings
from datetime import datetime

import pyautogui
import pyperclip
from pywinauto.application import Application
from rich.console import Console

from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.util import (
    api_simplifica,
    find_element_center,
    find_target_position,
    kill_process,
    login_emsys,
    take_sreenshot,
    take_target_position,
    type_text_into_field,
)

console = Console()

ASSETS_BASE_PATH = 'assets/descartes_transferencias_images/'
ALMOXARIFADO_DEFAULT = "50"

async def descartes(task):
    try:
        #Inicializa variaveis
        pre_venda_message = None
        nota_fiscal = None
        log_msg = None
        valor_nota = None
        #Get config from BOF
        config = await get_config_by_name("Descartes_Emsys")
        itens = task['configEntrada']['itens']

        # Obtém a resolução da tela
        screen_width, screen_height = pyautogui.size()

        # Print da resolução
        console.print(f"Largura: {screen_width}, Altura: {screen_height}")

        # Abre um novo emsys
        await kill_process("EMSys")
        app = Application(backend='win32').start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings("ignore", category=UserWarning, message="32-bit application should be automated using 32-bit Python")
        console.print("\nEMSys iniciando...", style="bold green")
        return_login = await login_emsys(config['conConfiguracao'], app, task)
        
        if return_login['sucesso'] == True:
            type_text_into_field('Cadastro Pré Venda', app['TFrmMenuPrincipal']['Edit'], True, '50')
            pyautogui.press('enter')
            time.sleep(1)
            pyautogui.press('enter')
            console.print(f"\nPesquisa: 'Cadastro Pre Venda' realizada com sucesso", style="bold green")
        else:
            logger.info(f"\nError Message: {return_login["retorno"]}")
            console.print(f"\nError Message: {return_login["retorno"]}", style="bold red")
            return return_login

        time.sleep(7)

        #Preenche data de validade
        screenshot_path = take_sreenshot()
        target_pos = find_target_position(screenshot_path, "Validade", 10, 0, 15) 
        if target_pos == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de validade"}
        
        pyautogui.click(target_pos)
        pyautogui.write(f'{datetime.now().strftime("%d/%m/%Y")}', interval=0.1)
        pyautogui.press('tab')
        console.print(f"\nValidade Digitada: '{datetime.now().strftime("%d/%m/%Y")}'", style="bold green")
        time.sleep(1)
        # field_validade = await find_element_center(ASSETS_BASE_PATH + "field_validade.png", (881, 292, 143, 57), 15)
        # if field_validade is not None:
        #     pyautogui.click(field_validade.x, field_validade.y)
        #     pyautogui.write(f'{datetime.now().strftime("%d/%m/%Y")}', interval=0.1)
        #     pyautogui.press('tab')
        #     console.print(f"\nValidade Digitada: '{datetime.now().strftime("%d/%m/%Y")}'", style="bold green")
        #     time.sleep(1)
        # else:
        #     observacao = f"\nCampo 'Validade' não encontrado"
        #     logger.info(f'{observacao}')
        #     console.print(f"{observacao}", style="bold red")
        #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        #     return {"sucesso": False, "retorno": observacao}

        #Condição da Pré-Venda
        # condicao_field = await find_element_center(ASSETS_BASE_PATH + "condicao_pre_venda_descartes.png", (976, 281, 248, 63), 15)
        condicao_field = find_target_position(screenshot_path, "Condição", 10, 0, 15) 
        if condicao_field == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar o campo de condição"}
        pyautogui.click(condicao_field)
        time.sleep(1)
        pyautogui.write("A")
        time.sleep(1)
        pyautogui.press("down")
        pyautogui.press("enter")
        time.sleep(1)
        # screenshot_path = take_sreenshot()
        # a_vista_option_position = find_target_position(screenshot_path, "VISTA", attempts=15)
        # if a_vista_option_position == None:
        #     return {"sucesso": False, "retorno": f"Não foi possivel encontrar a opção A Vista"}
        
        # pyautogui.click(a_vista_option_position)

        # if condicao_field is not None:
        #     pyautogui.click(condicao_field.x, condicao_field.y)
        #     pyautogui.sleep(1)
        #     transferencia = await find_element_center(ASSETS_BASE_PATH + "a_vista_descartes.png", (977, 281, 232, 171), 15)
        #     pyautogui.click(transferencia.x, transferencia.y)
        #     pyautogui.sleep(1)
        #     console.print(f"\nCondição 'A Vista' Selecionada", style="bold green")
        # else:
        #     logger.info(f"\nError Message: Campo 'Condicao pre-venda' não encontrado")
        #     console.print(f"\nError Message: Campo 'Condicao pre-venda' não encontrado", style="bold red")

        #Preenche o campo do cliente com o número da filial
        screenshot_path = take_sreenshot()
        cliente_field_position = (880, 383) #find_target_position(screenshot_path, "Cliente", 0, 160, 15)
        if cliente_field_position == None:
            return {"sucesso": False, "retorno": f"Não foi possivel encontrar a o campo cliente"}
        pyautogui.click(cliente_field_position)
        pyautogui.hotkey("ctrl", "a")
        pyautogui.hotkey("del")
        pyautogui.write(task['configEntrada']['filialEmpresaOrigem'])
        pyautogui.hotkey("tab")
        time.sleep(6)

        # cliente_field = await find_element_center(ASSETS_BASE_PATH + "field_cliente.png", (795, 354, 128, 50), 15)
        # if cliente_field is not None:
        #     pyautogui.click(cliente_field.x, cliente_field.y)
        #     pyautogui.hotkey("ctrl", "a")
        #     pyautogui.hotkey("del")
        #     pyautogui.write(task['configEntrada']['filialEmpresaOrigem'])
        #     pyautogui.hotkey("tab")
        #     console.print(f"\nCliente preenchido: '{task['configEntrada']['filialEmpresaOrigem']}'", style="bold green")
        #     time.sleep(6)
        # else:
        #     logger.info(f"\nError Message: Campo 'Cliente' não encontrado")
        #     console.print(f"\nError Message: Campo 'Cliente' não encontrado", style="bold red")

        #Verifica se precisa selecionar endereço
        screenshot_path = take_sreenshot()
        window_seleciona_endereco_position = take_target_position(screenshot_path, "Endereço")
        if window_seleciona_endereco_position is not None:
            log_msg = f'Aviso para selecionar Endereço'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}
        else:
            log_msg = "Sem Aviso de Seleção de Endereço"
            console.print(log_msg, style='bold green')
            logger.info(log_msg)

        # window_seleciona_endereco = await find_element_center(ASSETS_BASE_PATH + "window_selecionar_endereco.png", (569, 350, 785, 340), 10)
        # if window_seleciona_endereco is not None:
        #     observacao = f'Aviso para selecionar Endereço'
        #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        #     return {"sucesso": False, "retorno": observacao}
        # else:
        #     console.print("Sem Aviso de Seleção de Endereço", style='bold green')
        #     logger.info("Sem Aviso de Seleção de Endereço")
        
        # Clica em cancelar na Janela "Busca Representante"
        screenshot_path = take_sreenshot()
        window_busca_representante_position = take_target_position(screenshot_path, "Representante")
        if window_busca_representante_position is not None:
            button_cancelar_position = find_target_position(screenshot_path, "Cancelar", attempts=15)            
            pyautogui.click(button_cancelar_position)
        
        time.sleep(2)

        # window_busca_representante = await find_element_center(ASSETS_BASE_PATH + "window_busca_representante.png", (695, 342, 537, 106), 20)
        # if window_busca_representante is not None:
        #     button_cancelar = await find_element_center(ASSETS_BASE_PATH + "button_cancelar.png", (691, 342, 534, 343), 15)
        #     pyautogui.click(button_cancelar.x, button_cancelar.y)
        
        # time.sleep(2)

        # Aviso "Deseja alterar a condição de pagamento informada no cadastro do cliente?"
        screenshot_path = take_sreenshot()
        payment_condition_warning_position = take_target_position(screenshot_path, "pagamento")
        if payment_condition_warning_position is not None:
            button_no_position = (999, 568) #find_target_position(screenshot_path, "No", attempts=15)            
            pyautogui.click(button_no_position)
            console.print(f"\nClicou 'No' Mensagem 'Deseja alterar a condição de pagamento informada no cadastro do cliente?'", style="bold green")
            time.sleep(6)
        else:
            log_msg = f"\nError Message: Aviso de condição de pagamento não encontrado"
            logger.info(log_msg)
            console.print(log_msg, style="bold red")

        # payment_condition_warning = await find_element_center(ASSETS_BASE_PATH + "warning_change_payment_condition.png", (627, 420, 674, 192), 15)
        # if payment_condition_warning is not None:
        #     button_no = await find_element_center(ASSETS_BASE_PATH + "warning_button_no.png", (627, 420, 674, 192), 15)
        #     pyautogui.click(button_no.x, button_no.y)
        #     console.print(f"\nClicou 'No' Mensagem 'Deseja alterar a condição de pagamento informada no cadastro do cliente?'", style="bold green")
        #     time.sleep(6)
        # else:
        #     logger.info(f"\nError Message: Aviso de condição de pagamento não encontrado")
        #     console.print(f"\nError Message: Aviso de condição de pagamento não encontrado", style="bold red")

        time.sleep(3)

        #Seleciona 'Custo Médio' (Seleção do tipo de preço)
        screenshot_path = take_sreenshot()
        custo_medio_select_position = (851, 523) #find_target_position(screenshot_path, "Médio", attempts=15)
        if custo_medio_select_position is not None:
            pyautogui.click(custo_medio_select_position)
            button_ok_position = (1042, 583) #find_target_position(screenshot_path, "OK", attempts=15)            
            pyautogui.click(button_ok_position)
            time.sleep(5)
            console.print(f"\nClicou OK 'Custo médio'", style="bold green")
        else:
            log_msg = f"\nError Message: Campo 'Custo Médio' não encontrado"
            logger.info(log_msg)
            console.print(log_msg, style="bold yellow")

        time.sleep(10)

        # custo_medio_select = await find_element_center(ASSETS_BASE_PATH + "select_custo_medio.png", (826, 430, 276, 179), 15)
        # if custo_medio_select is not None:
        #     pyautogui.click(custo_medio_select.x, custo_medio_select.y)
        #     button_ok = await find_element_center(ASSETS_BASE_PATH + "select_ok_custo_medio.png", (826, 430, 276, 179), 15)
        #     pyautogui.click(button_ok.x, button_ok.y)
        #     time.sleep(5)
        #     console.print(f"\nClicou OK 'Custo médio'", style="bold green")
        # else:
        #     logger.info(f"\nError Message: Campo 'Custo Médio' não encontrado")
        #     console.print(f"\nError Message: Campo 'Custo Médio' não encontrado", style="bold yellow")

        # time.sleep(10)

        #Clica em ok na mensagem "Existem Pré-Vendas em aberto para este cliente."
        screenshot_path = take_sreenshot()
        existing_pre_venda_position = find_target_position(screenshot_path, "Pré-Vendas", attempts=15)
        if existing_pre_venda_position is not None:
            button_ok_position = (962, 562) #find_target_position(screenshot_path, "OK", attempts=15)            
            pyautogui.click(button_ok_position)
            console.print(f"\nClicou OK 'Pre Venda Existente'", style="bold green")
            time.sleep(5)
        else:
            log_msg = f"\nError Message: Menssagem de prevenda existente não encontrada"
            logger.info(log_msg)
            console.print(log_msg, style="bold yellow")


        # existing_pre_venda = await find_element_center(ASSETS_BASE_PATH + "existing_pre_venda.png", (831, 437, 247, 156), 15)
        # if existing_pre_venda is not None:
        #     button_ok = await find_element_center(ASSETS_BASE_PATH + "button_ok.png", (831, 437, 247, 156), 15)
        #     pyautogui.click(button_ok.x, button_ok.y)
        #     console.print(f"\nClicou OK 'Pre Venda Existente'", style="bold green")
        #     time.sleep(5)
        # else:
        #     logger.info(f"\nError Message: Menssagem de prevenda existente não encontrada")
        #     console.print(f"\nError Message: Menssagem de prevenda existente não encontrada", style="bold yellow")

        #Define representante para "1"
        screenshot_path = take_sreenshot()
        field_representante_position = find_target_position(screenshot_path, "Representante", 0, 50, attempts=15)
        if field_representante_position is not None:
            pyautogui.doubleClick(field_representante_position)
            pyautogui.hotkey("ctrl", "a")
            pyautogui.hotkey("del")
            pyautogui.write('1')
            pyautogui.hotkey("tab")
        
        time.sleep(3)


        # field_representante = await find_element_center(ASSETS_BASE_PATH + "field_representante.png", (679, 416, 214, 72), 15)
        # if field_representante is not None:
        #     pyautogui.doubleClick(field_representante.x + 50, field_representante.y + 1)
        #     pyautogui.hotkey("ctrl", "a")
        #     pyautogui.hotkey("del")
        #     pyautogui.write('1')
        #     pyautogui.hotkey("tab")
        
        # time.sleep(3)

        #Seleciona modelo de capa
        screenshot_path = take_sreenshot()
        model_descarte_position = (848, 527) #find_target_position(screenshot_path, "Modelo", 0, 100, attempts=15)
        if model_descarte_position is not None:
            pyautogui.click(model_descarte_position)
            pyautogui.click(1500, 800)
            pyautogui.write("B")
            pyautogui.hotkey("tab")
        else:
            log_msg = f'Campo Modelo na capa da nota não encontrado'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}

        # model_descarte = await find_element_center(ASSETS_BASE_PATH + "field_modelo_faturamento.png", (681, 489, 546, 96), 15)
        # if model_descarte is not None:
        #     pyautogui.click(model_descarte.x + 100, model_descarte.y)
        #     pyautogui.click(1500, 800)
        #     pyautogui.write("B")
        #     pyautogui.hotkey("tab")
        # else:
        #     observacao = f'Campo Modelo na capa da nota não encontrado'
        #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        #     return {"sucesso": False, "retorno": observacao}

        #Abre Menu itens
        menu_itens = (570, 317) #find_target_position(screenshot_path, "Itens", 0, 0, attempts=15)
        if menu_itens is not None:
            pyautogui.click(menu_itens)
        else:
            log_msg = f'Campo "Itens" no menu da pré-venda não encontrado'
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}

        time.sleep(2)

        #Loop de itens
        for item in itens:
            screenshot_path = take_sreenshot()
            #Clica no botão inclui para abrir a tela de item
            button_incluir = (905, 573) #find_target_position(screenshot_path, "Incluir", 0, 0, attempts=15)
            if button_incluir is not None:
                pyautogui.click(button_incluir)
                console.print("\nClicou em 'Incluir'", style='bold green')            
            else:
                log_msg = f'Botão "Incluir" não encontrado'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}
            time.sleep(3)
            
            screenshot_path = take_sreenshot()
            # Digita Almoxarifado
            field_almoxarifado = (839, 313) #find_target_position(screenshot_path, "Almoxarifado",0, 129, 15)
            if field_almoxarifado is not None:
                pyautogui.doubleClick(field_almoxarifado)
                pyautogui.hotkey('del')
                pyautogui.write(task['configEntrada']['filialEmpresaOrigem'] + ALMOXARIFADO_DEFAULT)
                pyautogui.hotkey('tab')
                time.sleep(2)
                console.print(f"\nDigitou almoxarifado {task['configEntrada']['filialEmpresaOrigem'] + ALMOXARIFADO_DEFAULT}", style='bold green')            
            else:
                log_msg = f'Campo Almoxarifado não encontrado'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}

            #Segue para o campo do item
            field_item = (841, 339) #find_target_position(screenshot_path, "Item", 0, 130, 15)
            if field_item is not None:
                pyautogui.doubleClick(field_item)
                pyautogui.hotkey('del')
                pyautogui.write(item['codigoProduto'])
                pyautogui.hotkey('tab')
                time.sleep(2)
                console.print(f"\nDigitou item {item['codigoProduto']}", style='bold green')
            else:
                log_msg = f'Campo Item não encontrado.'
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": log_msg}

            screenshot_path = take_sreenshot()

            #Checa tela de pesquisa de item
            window_pesquisa_item = await find_element_center(ASSETS_BASE_PATH + "window_pesquisa_item.png", (488, 226, 352, 175), 10)
            console.log(f"Produto {item['codigoProduto']} encontrado", style="bold green")
            logger.info(f"Produto {item['codigoProduto']} encontrado")

            if window_pesquisa_item is not None:
                observacao = f"Item {item['codigoProduto']} não encontrado, verificar cadastro"
                console.log(f"{observacao}", style="bold green")
                logger.info(f"{observacao}")
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": observacao}

            #Tela Pesquisa item
            # window_pesquisa_item = take_target_position(screenshot_path, "Pesquisa")
            # if window_pesquisa_item is not None:
            #     log_msg = f'Item não encontrado.'
            #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            #     return {"sucesso": False, "retorno": log_msg}
            # else:
            #     console.print(f"Item encontrado!", style='bold green')
                
            #Checa se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)
            warning_price = await find_element_center(ASSETS_BASE_PATH + "warning_item_price.png",  (824, 426, 255, 191), 10)
            if warning_price is not None:
                observacao = f"Item {item['codigoProduto']} não possui preço, verificar erro de estoque ou de bloqueio."
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", observacao, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                return {"sucesso": False, "retorno": observacao}
            
            screenshot_path = take_sreenshot()
            
            #Checa se existe alerta de item sem preço, se existir retorna erro(simplifica e bof)
            # window_preco = take_target_position(screenshot_path, "preço")
            # if window_preco is not None:
            #     log_msg = f'Item {item['codigoProduto']} não possui preço, verificar erro de estoque ou de bloqueio.'
            #     await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            #     return {"sucesso": False, "retorno": log_msg}
            # else:
            #     console.print(f"Item sem alerta de preço!", style='bold green')
            
            time.sleep(2)

            screenshot_path = take_sreenshot()
            #Seleciona o Saldo Disponivel e verifica se ah possibilidade do descarte
            field_saldo_disponivel = (916, 606) #find_target_position(screenshot_path + "Saldo", 20, 0, 10)
            if field_saldo_disponivel is not None:
                pyautogui.doubleClick(field_saldo_disponivel)
                time.sleep(1)
                pyautogui.doubleClick(field_saldo_disponivel)
                time.sleep(1)
                pyautogui.hotkey('ctrl', 'c')
                amount_avaliable= ''
                amount_avaliable = pyperclip.paste()
                console.print(f"Saldo Disponivel: '{amount_avaliable}'", style="bold green")

                #Verifica se o saldo disponivel é valido para descartar
                if int(amount_avaliable) > 0 and int(amount_avaliable) >= int(item['qtd']): 
                    field_quantidade = (1047, 606) #find_target_position(screenshot_path, "Quantidade", 20, 0, 15)
                    pyautogui.doubleClick(field_quantidade)
                    pyautogui.hotkey('del')
                    pyautogui.write(str(item['qtd']))
                    pyautogui.hotkey('tab')
                    time.sleep(2)
                else:
                    log_msg = f"Saldo disponivel: '{amount_avaliable}' é menor que '{item['qtd']}' o valor que deveria ser descartado. Item: '{item['codigoProduto']}'"
                    await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                    console.print(log_msg, style="bold red")
                    return {"sucesso": False, "retorno": log_msg}

            #Clica em incluir para adicionar o item na nota
            button_incluir_item = (1007, 745) #find_target_position(screenshot_path, "Inlcuir", 0, 0, 15)
            if button_incluir_item is not None:
                pyautogui.click(button_incluir_item)
                time.sleep(2)
            else:
                log_msg = f"Botao 'Incluir' item não encontrado"
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                console.print(log_msg, style="bold red")
                return {"sucesso": False, "retorno": log_msg}
            
            #Clica em cancelar para fechar a tela e abrir novamente caso houver mais itens
            button_cancela_item = (1194, 745) #find_target_position(screenshot_path, "Cancela", 0, 0, 15)
            if button_cancela_item is not None:
                pyautogui.click(button_cancela_item)
                time.sleep(2)
            else:
                log_msg = f"Botao cancelar para fechar a tela do item nao encontrado"
                await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
                console.print(log_msg, style="bold red")
                return {"sucesso": False, "retorno": log_msg}
            
        time.sleep(2)

        #Clica no botão "+" no canto superior esquerdo para lançar a pre-venda
        #Precisa manter por imagem pois não tem texto
        button_lanca_pre_venda = await find_element_center(ASSETS_BASE_PATH + "button_lanca_prevenda.png", (490, 204, 192, 207), 15)
        if button_lanca_pre_venda is not None:
            pyautogui.click(button_lanca_pre_venda.x, button_lanca_pre_venda.y)
            console.print("\nLançou Pré-Venda", style="bold green")
        else:
            log_msg = f"Botao lança pre-venda nao encontrado"
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": log_msg}
        
        time.sleep(5)

        screenshot_path = take_sreenshot()

       #Verifica mensagem de "Pré-Venda incluida com número: xxxxx"
        included_pre_venda = find_target_position(screenshot_path, "incluída", attempts=15)
        if included_pre_venda is not None:
            #Clica no centro da mensagem e copia o texto para pegar o numero da pre-venda
            pyautogui.click(included_pre_venda)
            pyautogui.hotkey("ctrl", "c")
            pre_venda_message = pyperclip.paste()
            pre_venda_message = re.findall(r'\d+-\d+', pre_venda_message)
            console.print(f"Numero pré-venda: '{pre_venda_message[0]}'",style='bold green')
            #Clica no ok da mensagem
            button_ok = (1064, 604) #find_target_position(screenshot_path, "Ok", 15)
            pyautogui.click(button_ok)
        else:
            log_msg = f"Não achou mensagem Pré-Venda incluida."
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            console.print(log_msg, style="bold red")
            return {"sucesso": False, "retorno": log_msg}
        
        screenshot_path = take_sreenshot()

        #Message 'Deseja pesquisar pré-venda?'
        message_prevenda = take_target_position(screenshot_path, "Deseja")
        if message_prevenda is not None:
            button_yes = find_target_position(screenshot_path, "Yes", attempts=15)
            pyautogui.click(button_yes)
        else:
            log_msg = f"Mensagem 'Deseja pesquisar pré-venda?' não encontrada."
            console.print(log_msg, style="bold yellow")
        
        screenshot_path = take_sreenshot()
        #Confirma pré-venda
        #Pode não precisar em descartes, mas em trânsferencias é obrigatório
        button_confirma_transferencia = take_target_position(screenshot_path, "confirma")
        if button_confirma_transferencia is not None:
            pyautogui.click(button_confirma_transferencia)
            console.log("Confirmou transferencia", style="bold green")
        else:
            log_msg = f"Botao 'Confirma' não encontrado"
            console.print(log_msg, style="bold yellow")
        
        pyautogui.moveTo(1200, 300)

        screenshot_path = take_sreenshot()

        #TODO Partir daqui
        message_confirma_transferencia = take_target_position(screenshot_path, "confirmar")
        if message_confirma_transferencia is not None:
            #clica em sim na mensagem
            button_yes= find_target_position(screenshot_path, "Yes", attempts=15)
            pyautogui.click(button_yes)
            console.log("Cliclou em 'Sim' para cofirmar a pré-venda", style='bold green')
            pyautogui.moveTo(1200, 300)
            time.sleep(2)
            screenshot_path = take_sreenshot()
            vencimento_message_primeira_parcela = take_target_position(screenshot_path, "vencimento")
            #TODO apareceu em dev apenas pode nao ser necesário em prod mantive por segurança
            #Pode nao aparecer na prod
            if vencimento_message_primeira_parcela is not None:
                button_yes = find_target_position(screenshot_path, "Yes", attempts=15)
                pyautogui.click(button_yes)
            time.sleep(2)
            screenshot_path = take_sreenshot()
            #Clica no OK 'Pre-Venda incluida com sucesso'
            button_ok = find_target_position(screenshot_path, "Ok", attempts=15)
            pyautogui.click(button_ok)
            console.log("Cliclou em 'OK' para pré-venda confirmada com sucesso", style='bold green')
        else:
            log_msg = f"Mensagem 'Deseja realmente confirmar esta pré-venda?' não encontrada."
            console.print(log_msg, style="bold yellow")

        pyautogui.moveTo(1000, 500)

        screenshot_path = take_sreenshot()
        #Clica em Faturar
        button_faturar = (1313, 395) #find_target_position(screenshot_path, "Faturar", attempts=15)
        if button_faturar is not None:
            time.sleep(2)
            pyautogui.click(button_faturar)
            console.print(f"Clicou em: 'Faturar'",style='bold green')
        else:
            log_msg = f"Não encontrou botão faturar"
            console.print(log_msg, style="bold yellow")
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": f'{log_msg}'}
         
        time.sleep(10)

        screenshot_path = take_sreenshot()

        #Verifica se existe a mensagem de recalcular parcelas
        message_recalcular = find_target_position(screenshot_path, "Recalcular", attempts=15)
        #Se existir clica em nao
        if message_recalcular is not None:
            button_no = (999, 560) #find_target_position(screenshot_path, "No", attempts=15)
            pyautogui.click(button_no)
            console.log("Cliclou em 'No' na mensagem de recalcular parcelas", style="bold green") 
        else:
            logger.info(f"Mensagem de para recalcular parcelas da pre-venda nao existe")
            console.print(f"Mensagem de para recalcular parcelas da pre-venda nao existe", style="bold yellow")
        
        time.sleep(8)
        screenshot_path = take_sreenshot()

        #TODO apareceu em dev apenas pode nao ser necesário em prod mantive por segurança
        # Warning 'Atribuir o valor da Substituição tributária na Primeira Parcela?'
        warning_substituicao_trib = take_target_position(screenshot_path, "tributária")
        if warning_substituicao_trib is not None:
            console.log("Vai clicar em não")
            button_no = find_target_position(screenshot_path,"Não", attempts=15)
            pyautogui.click(button_no)
            console.log("Cliclou em 'No' na mensagem de Substiucao tributaria", style="bold green")
        else:
            console.log("Sem aviso apresentado! 'Atribuir o valor da Substituição tributária na Primeira Parcela?'", style="bold green")

        time.sleep(3)
        modelo_select_position = (874,267)
        pyautogui.click(modelo_select_position)
        pyautogui.write("N")
        time.sleep(1)
        for _ in range(3):
            pyautogui.press('down')
        pyautogui.press('enter')

        # screenshot_path = take_sreenshot()
        
        # model_selected = find_target_position(screenshot_path, "77", attempts=15)
        # if model_selected is None:
        #     console.print("Selecionando Modelo", style="bold green")
        #     # field_modelo_faturamento = find_target_position(screenshot_path, "modelo", 0, 200, 15)
        #     if model_selected is not None:
        #         pyautogui.click(model_selected)
        #         # pyautogui.click(field_modelo_faturamento)
        #         # time.sleep(1)
        #         # for _ in range(15):
        #         #     pyautogui.keyDown('up')
        #         # pyautogui.keyUp('up')
        #         # screenshot_path = take_sreenshot()                 
        #         # model_to_select = find_target_position(screenshot_path, "077", attempts=15)
        #         # pyautogui.click(model_to_select)

        #     else:
        #         log_msg = {
        #         "Numero Pre Venda": pre_venda_message[0],
        #         "Numero da nota": None
        #         }
        #         await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
        #         return {"sucesso": False, "retorno": "Falha ao selecionar modelo: Na tela de Faturamento Pré-Venda"}
        # else:
        #     console.log("Modelo da nota já selecionado", style="bold green")
        
        time.sleep(5)

        #Pega total da Nota
        #Vou manter no antigo ainda para facilitar, pois existe mais de um campo "total" na tela
        field_total_nota = await find_element_center(ASSETS_BASE_PATH + "field_total_nota.png", (1067, 767, 306, 98), 15)
        if field_total_nota is not None:
            pyautogui.click(field_total_nota.x, field_total_nota.y)
            pyautogui.doubleClick(field_total_nota.x + 35, field_total_nota.y)
            pyautogui.hotkey("ctrl", "c")
            valor_nota = pyperclip.paste()
            valor_nota = re.findall(r'\b\d{1,3}(?:\.\d{3})*,\d{2}\b', valor_nota)
            console.print(f"\nValor NF: '{valor_nota[0]}'",style='bold green')
        else:
            console.print(f"\nNão conseguiu extrair o valor da nota",style='bold red')
            logger.info("\nNão conseguiu extrair o valor da nota")

        #Clicar no botao "OK" com um certo verde
        screenshot_path = take_sreenshot()
        
        button_verde = (1180, 822) #find_target_position(screenshot_path, "Ok", attempts=15)
        if button_verde is not None:
            pyautogui.click(button_verde)
        else:
            log_msg = f"Não conseguiu achar botão 'OK'"
            console.print(log_msg)
            logger.info(log_msg)
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal, valor_nota)
            return {"sucesso": False, "retorno": log_msg}
    
        time.sleep(5)

        screenshot_path = take_sreenshot()

        #Aviso "Deseja faturar pré-venda?"
        faturar_pre_venda = find_target_position(screenshot_path, "realmente", attempts=15)
        if faturar_pre_venda is not None:
            button_yes = (918, 561) #find_target_position(screenshot_path, "yes", attempts=15)
            pyautogui.click(button_yes)
        else:
            log_msg = {
            "numero_pre_venda": pre_venda_message[0],
            "numero_nota": ''
            }
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota[0])
            return {"sucesso": False, "retorno": "Falha ao cliclar em: 'SIM' no aviso: 'Deseja realmente faturar esta Pré-Venda ?'"}

        screenshot_path = take_sreenshot()

        #Mensagem de nota fiscal gerada com número
        screenshot_path = take_sreenshot()
        nota_fiscal_gerada = find_target_position(screenshot_path, "gerada", attempts=15)
        pyautogui.click(nota_fiscal_gerada)
        pyautogui.hotkey("ctrl", "c")
        nota_fiscal = pyperclip.paste()
        nota_fiscal = re.findall(r'\d+-?\d*', nota_fiscal)
        console.print(f"\nNumero NF: '{nota_fiscal[0]}'",style='bold green')

        time.sleep(7)

        screenshot_path = take_sreenshot()

        #Transmitir a nota
        transmitir = find_target_position(screenshot_path, "transmitir", attempts=15)
        if transmitir is not None:
            pyautogui.click(transmitir)
            logger.info("\nNota Transmitida")
            console.print("\nNota Transmitida", style="bold green")
        else:
            log_msg = f'\nNota não Transmitida'
            logger.info(log_msg)
            console.print(log_msg ,style="bold red")
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota[0])
            return {"sucesso": False, "retorno": log_msg}

        time.sleep(7)

        screenshot_path = take_sreenshot()
        #Fechar transmitir nota
        transmitir_fechar = find_target_position(screenshot_path, "fechar", attempts=15)
        if transmitir_fechar is not None:
            pyautogui.click(transmitir_fechar)
            log_msg = f'Nota Transmitida com sucesso'
            logger.info(log_msg)
            console.print(log_msg)
        else:
            log_msg = f'Nota não transmitida'
            logger.info(log_msg)
            console.print(log_msg, style='bold red')
            await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota[0])
            return {"sucesso": False, "retorno": log_msg}

        log_msg = {
            "numero_pre_venda": pre_venda_message[0],
            "numero_nota": nota_fiscal[0],
            "valor_nota": valor_nota[0]
        }

        await api_simplifica(task['configEntrada']['urlRetorno'], "SUCESSO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota[0])
        return {"sucesso": True, "retorno": log_msg}
    
    except Exception as ex:
        log_msg = f"Erro Processo Descartes: {str(ex)}"
        logger.error(log_msg)
        console.print(log_msg, style="bold red")
        await api_simplifica(task['configEntrada']['urlRetorno'], "ERRO", log_msg, task['configEntrada']['uuidSimplifica'], nota_fiscal[0], valor_nota[0])
        return {"sucesso": False, "retorno": log_msg}

if __name__ == "__main__":
    task_fake = {'datEntradaFila': '2024-08-05T14:24:40.146-03:00', 'configEntrada': {'itens': [{'qtd': 1, 'codigoProduto': '36266', 'unidadeMedida': 'UN', 'descricaoProduto': 'COOKIE RED VELVET CHOC BRANCO 75G'}, {'qtd': 2, 'codigoProduto': '36265', 'unidadeMedida': 'UN', 'descricaoProduto': 'COOKIE CHOC AO LEITE CREME AVELA 75G'}, {'qtd': 6, 'codigoProduto': '6395', 'unidadeMedida': 'UN', 'descricaoProduto': 'PAO DE QUEIJO UN'}, {'qtd': 5, 'codigoProduto': '33931', 'unidadeMedida': 'UN', 'descricaoProduto': 'CAFE FILTRADO SIM 180ml'}, {'qtd': 1, 'codigoProduto': '33854', 'unidadeMedida': 'UN', 'descricaoProduto': 'EMPADA DE FRANGO COM REQUEIJAO 160G'}], 'processo': 'abcfa1ba-d580-465a-aefb-c15ac4514407', 'urlRetorno': 'https://public.simrede.com.br/simplifica/retornoRpa', 'cnpjEmpresa': '07473735020026', 'nomeEmpresa': 'Flores Videiras', 'dataDescarte': '2024-08-03T03:00:00', 'uuidSimplifica': 'd080ab9e-c045-4bc3-8aa6-cddad7487f1d', 'filialEmpresaOrigem': '200'}, 'uuidProcesso': 'abcfa1ba-d580-465a-aefb-c15ac4514407', 'nomProcesso': 'Sim Rede - Descarte no Emsys', 'uuidFila': '24f0c49f-bf79-4016-a616-e9566f2d575d'}

    asyncio.run(descartes(task_fake))