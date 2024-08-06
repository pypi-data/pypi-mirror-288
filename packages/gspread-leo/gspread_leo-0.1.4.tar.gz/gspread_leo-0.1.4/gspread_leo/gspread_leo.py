import gspread, os


if os.path.isfile(r'.\cliente.json'):
    credencial = r'.\cliente.json'
    gc = gspread.service_account(credencial)
# else:
#     raize ValueError('Arquivo "cliente.json" não encontrado')


def Abrir_planilha(key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8'):
    return gc.open_by_key(key)

def Criar_planilha(titulo):
    return gc.create(titulo)

def Selecionar_pagina(planilha, nome):
    return planilha.worksheet(nome)

def Criar_pagina(planilha, nome):
    return planilha.add_worksheet(title=nome, rows=100, cols=20)

def Deletar_pagina(planilha, pagina):
    planilha.del_worksheet(pagina)

def Ler_celulas(pagina, intervalo = "A1:B2"):
    return pagina.get(intervalo)

def Atualizar_celulas(pagina,intervaalo:str, valor:list[list] ):
    pagina.update(intervaalo, valor)



def Criar_pagina2(nome, key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', credencial = r'.\cliente.json'):
    return gspread.service_account(credencial).open_by_key(key).add_worksheet(title=nome, rows=100, cols=20)

def Ler_celulas2(intervalo = "A1:B2", key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', pagina = "campos do jordão", credencial = r'.\cliente.json'):
    return gspread.service_account(credencial).open_by_key(key).worksheet(pagina).get(intervalo)

def Atualizar_celulas2(valor:list[list],intervalo = "g1:h2", key = '1YAdc2ZefohO6o0532Tc34-huUIr5hUUS4WRXVmYDRZ8', pagina = "campos do jordão" , credencial = r'.\cliente.json'):
    gspread.service_account(credencial).open_by_key(key).worksheet(pagina).update(intervalo, valor)


def Ler_celulas3(intervalo = "A1:B2", url = 'https://docs.google.com/spreadsheets/d/1YfCG_ljMWHoE27Kw7Uw7TwkbWRqH4HnS1AGnQe7XLBs', pagina = "campos do jordão", credencial = r'.\cliente.json'):
    return gspread.service_account(credencial).open_by_url(url).worksheet(pagina).get(intervalo)

def Atualizar_celulas3(valor:list[list],intervalo = "g1:h2", url = 'https://docs.google.com/spreadsheets/d/1YfCG_ljMWHoE27Kw7Uw7TwkbWRqH4HnS1AGnQe7XLBs', pagina = "campos do jordão" , credencial = r'.\cliente.json'):
    gspread.service_account(credencial).open_by_url(url).worksheet(pagina).update(intervalo, valor)

def Criar_planilha3(titulo,credencial, email_propietario ):
    s = gspread.service_account(credencial).create(titulo)
    s.share(email_propietario, perm_type='user', role='writer')
    return s.url

def RenomearPagina(nome, num_pagina, url, credencial):
    worksheet = gspread.service_account(credencial).open_by_url(url).get_worksheet(num_pagina)
    worksheet.update_title(nome)


def Colorir(cor = (0.8,0.8,0.8), url,pagina, intervalo ="A1:G1",  credencial ):
    gspread.service_account(credencial).open_by_url(url).worksheet(pagina).format(intervalo, {
                                                                                    "backgroundColor": {
                                                                                    "red": cor[0],
                                                                                    "green": cor[1],
                                                                                    "blue": cor[2]
                                                                                    }
                                                                                })
    

