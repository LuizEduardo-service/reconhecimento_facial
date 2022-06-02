from os import system
import pathlib
import shutil
import sys
import time
import cv2
import easygui
from numpy import true_divide
from codigo.simple_facerec import SimpleFacerec
import pandas as pd


class ProgramaReconhecimentoFacial:
    def menu_inicial(self):
        system('cls')
        print('====================================================')
        print('        MINISTERIO DO MEIO AMBIENTE')
        print('====================================================')
        print(
            'ferramenta de identificação e autenticação biométrica que restrinja \n o acesso a uma rede com banco dados do Ministério do Meio Ambiente.\n'
        )

        print('[1]: Acesso Login restrito')
        print('[2]: Cadastro de Usuario Padrão')
        print(
            '=================================================================='
        )
        opc = str(
            input(
                "Digite a opção desejada para o acesso ou  'sair' para encerrar o programa: "
            )
        )

        if opc == '1':
            usu = self.valida_usuario()
            if usu != 'Unknown' and usu != '':
                self.acesso_usuario(usu)
        elif opc == '2':
            self.Cadastro_fotografia()
        elif opc == 'sair':
            print('Finalizando Programa...')
            time.sleep(2)
            system('cls')
            sys.exit()

    def Cadastro_fotografia(self):
        system('cls')
        print('====================================================')
        print('             CADASTRO DE USUARIOS')
        print('====================================================\n')
        camera_port = 0
        nFrames = 30
        camera = cv2.VideoCapture(camera_port)
        file = 'image/'
        nome = input('Digite seu nome: ')
        nivel = 1
        novo_usu = nome + ': ' + str(nivel)
        self.incluir_linha('outros\\acesso.txt', novo_usu)
        new_file = file + nome + '.png'
        print(
            "fique de frente para a camera e digite 's' para confirmar a imagem."
        )
        time.sleep(3)

        emLoop = True

        while emLoop:

            retval, img = camera.read()
            cv2.imshow('Foto', img)

            k = cv2.waitKey(100)

            if k == 27:
                emLoop = False

            elif k == ord('s'):
                cv2.imwrite(new_file, img)
                emLoop = False

        cv2.destroyAllWindows()
        camera.release()
        system('cls')
        print('Novo usuario Incluido')
        time.sleep(2)
        self.menu_inicial()

    def valida_usuario(self):
        sfr = SimpleFacerec()
        sfr.load_encoding_images('image/')
        cap = cv2.VideoCapture(0)
        usu_reco = False
        self.name = ''

        loops = True
        while loops:
            ret, frame = cap.read()

            face_locations, face_name = sfr.detect_known_faces(frame)
            for face_loc, self.name in zip(face_locations, face_name):
                if self.name == 'Unknown':
                    texto = 'Usuario inesistente!!'
                    usuario = 'Realize o cadastro e tente novamente.'
                    y1, x2, y2, x1 = (
                        face_loc[0],
                        face_loc[1],
                        face_loc[2],
                        face_loc[3],
                    )
                    cv2.putText(
                        frame,
                        texto,
                        (10, 60),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (255, 0, 0),
                        2,
                    )
                    cv2.putText(
                        frame,
                        usuario,
                        (10, 80),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (255, 0, 0),
                        1,
                    )
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(
                        frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED
                    )
                    cv2.putText(
                        frame,
                        self.name,
                        (x1 + 10, y2 - 10),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (255, 255, 255),
                        2,
                    )
                else:
                    texto = f'Usuario Reconhecido'
                    Usuario = f'bem vindo(a) {self.name}'
                    msg = f'Digite "s" para confirmar o acesso. '
                    y1, x2, y2, x1 = (
                        face_loc[0],
                        face_loc[1],
                        face_loc[2],
                        face_loc[3],
                    )
                    cv2.putText(
                        frame,
                        texto,
                        (10, 60),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (255, 0, 0),
                        2,
                    )
                    cv2.putText(
                        frame,
                        Usuario,
                        (10, 80),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (255, 0, 0),
                        1,
                    )
                    cv2.putText(
                        frame,
                        msg,
                        (10, 100),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1,
                        (255, 0, 0),
                        1,
                    )
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.rectangle(
                        frame, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED
                    )
                    cv2.putText(
                        frame,
                        self.name,
                        (x1 + 10, y2 - 10),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (255, 255, 255),
                        2,
                    )

                    usu_reco = True

            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1)
            if key == 27:
                cap.release()
                cv2.destroyAllWindows()
                self.menu_inicial()
            elif key == ord('s') and usu_reco == True:
                loops = False
                cap.release()
                cv2.destroyAllWindows()
                return self.name

    def ler_linha(self, path):
        try:
            mydict = {}
            with open(path, mode='r', encoding='utf-8') as inp:
                for line in inp:
                    try:
                        (key, val) = line.split(':')
                        mydict[key] = val.rstrip('\n').lstrip()
                    except ValueError:
                        pass
            return mydict
        except:
            print('Não foi possivel ler os dados')
            time.sleep(1)

    def incluir_linha(self, path, texto):
        with open(path, mode='a', encoding='utf-8') as arq:
            arq.write('\n' + texto)
        print('Valor incluido com Sucesso!')
        time.sleep(1)

    def excluir_linha(self, path, texto):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                try:
                    lines.remove(texto + '\n')
                except:
                    lines.remove(texto)
                with open(path, 'w', encoding='utf-8') as new_f:
                    for line in lines:
                        new_f.write(line)
            print('Dados excluido com Sucesso.')
        except:
            print('Não foi Possivel remover o valor.')
            time.sleep(1)

    def insere_usuario(self, nome):

        diretorio = easygui.fileopenbox()
        ext = pathlib.Path(diretorio).suffix
        if ext in ['.png', '.jpg', '.jpeg']:
            shutil.copy(diretorio, 'image' + '\\' + nome + '.png')
            print('Usuario inserido com Sucesso!!')
            time.sleep(3)
        else:
            print('Imagem não identificada!!')

    def acesso_usuario(self, usuario):
        system('cls')
        print('====================================================')
        print('             ACESSO DE USUARIOS')
        print('====================================================\n')
        lista = self.ler_linha('outros\\acesso.txt')
        nivel = lista.get(usuario)
        if nivel == '1':
            cargo = 'Usuario Padrão'
        elif nivel == '2':
            cargo = 'diretor de divisão'
        else:
            cargo = 'ministro do meio ambiente'

        opc = ''
        system('cls')
        if nivel == '1':
            print('====================================================')
            print('Ministério do Meio Ambiente acesso de nivel 1')
            print('====================================================')
            print(f'Usuario: {usuario}')
            print(f'Cargo: {cargo}')
            print('[1]: Resumo ')
            opc = str(input('Digite a opção desejada: '))
        if nivel == '2':
            print('====================================================')
            print('Ministério do Meio Ambiente acesso de nivel 2')
            print('====================================================')
            print(f'Usuario: {usuario}')
            print(f'Cargo: {cargo}')
            print('[1]: Resumo ')
            print(
                '[2]: Uso de pesticidas: quantidade total (em 1 mil toneladas) – médias móveis centradas (três anos)'
            )
            print(
                '[3]: Uso de pesticidas: quantidade aplicada por área cultivada – médias móveis centradas'
            )
            print(
                '[4]: Quantidade aplicada por área cultivada, por UF – médias móveis centradas (três anos)'
            )

            opc = str(input('Digite a opção desejada: '))
        if nivel == '3':
            print('====================================================')
            print('Ministério do Meio Ambiente acesso de nivel 3')
            print('====================================================')
            print(f'Usuario: {usuario}')
            print(f'Cargo: {cargo}')
            print('[1]: Resumo ')
            print(
                '[2]: Uso de pesticidas: quantidade total (em 1 mil toneladas) – médias móveis centradas (três anos)'
            )
            print(
                '[3]: Uso de pesticidas: quantidade aplicada por área cultivada – médias móveis centradas'
            )
            print(
                '[4]: Quantidade aplicada por área cultivada, por UF – médias móveis centradas (três anos)'
            )
            print('[5]: Inserir novo usuario')
            opc = str(input('Digite a opção desejada: '))

        if nivel == 1 and opc > 1:
            print(
                'Acesso negado!! Usuario nõ possui nivel de acesso suficiente para executar esta ação.'
            )
        elif nivel == 2 and opc > 4:
            print(
                'Acesso negado!! Usuario nõ possui nivel de acesso suficiente para executar esta ação.'
            )
        elif opc == 'sair':
            print('Finalizando Programa...')
            time.sleep(2)
            system('cls')
            sys.exit()
        else:
            self.menu(opc)

    def menu(self, opc):
        system('cls')
        opc2 = ''
        if opc == '1':
            print(
                '=============================================================================================='
            )
            print('                            RESUMO DE DADOS AGROTOXICOS')
            print(
                '=============================================================================================='
            )
            with open('documentos\intro.txt', 'r', encoding='utf-8') as f:
                for lin in f:
                    print(lin.rstrip('\n'))

        if opc == '2':
            print(
                '=============================================================================================='
            )
            print(
                'Uso de pesticidas: quantidade total (em 1 mil toneladas) – médias móveis centradas (três anos)'
            )
            print(
                '=============================================================================================='
            )
            df = pd.DataFrame(
                pd.read_excel(
                    'documentos\dados.xlsx', sheet_name='Uso de pesticidas'
                )
            )
            print(df)
        elif opc == '3':
            print(
                '=============================================================================================='
            )
            print(
                '    Uso de pesticidas: quantidade aplicada por área cultivada – médias móveis centradas'
            )
            print(
                '=============================================================================================='
            )
            df = pd.DataFrame(
                pd.read_excel(
                    'documentos\dados.xlsx', sheet_name='Uso de pesticidas 2'
                )
            )
            print(df)
        elif opc == '4':
            print(
                '=============================================================================================='
            )
            print(
                '     Quantidade aplicada por área cultivada, por UF – médias móveis centradas (três anos)'
            )
            print(
                '=============================================================================================='
            )
            df = pd.DataFrame(
                pd.read_excel(
                    'documentos\dados.xlsx', sheet_name='Uso de pesticidas 3'
                )
            )
            print(df)
        elif opc == '5':
            usu = input('Nome do Usuario: ')
            nivel = str(
                input(
                    'Informe o nivel de acesso do usuario cadastrado  (1 a 3): '
                )
            )
            novo_usu = usu + ': ' + str(nivel)
            if usu != '' and nivel in ['1', '2', '3']:
                self.insere_usuario(usu)
                self.incluir_linha('outros\\acesso.txt', novo_usu)
            else:
                print(
                    'Não foi possivel inserir novo usuario, verifique os dados e tente novamente.'
                )
        elif opc == 'sair':
            system('cls')
            self.encerra_programa()

        while True:
            print(
                '\n============================================================================'
            )
            sair = input(
                'Pressione "Enter" para sair ou digite "s" para voltar ao menu inicial:'
            )
            if not sair:
                print('Programa Finalizado...')
                time.sleep(3)
                sys('cls')
                sys.exit()
            else:
                self.acesso_usuario(self.name)

    def encerra_programa(self):
        while True:
            print(
                '\n============================================================================'
            )
            sair = input(
                'Pressione "Enter" para sair ou digite "s" para voltar ao menu inicial:'
            )
            if not sair:
                print('Programa Finalizado...')
                time.sleep(3)
                system('cls')
                sys.exit()
            else:
                self.menu_inicial()


try:
    program = ProgramaReconhecimentoFacial()
    program.menu_inicial()
except KeyboardInterrupt:
    print('\nPrograma Finalizado.')
