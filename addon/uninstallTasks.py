import os
import sys
import shutil
import gui
import wx

def onUninstall():
	# Caminho do NVDA (raiz onde está nvda.exe)
	nvda_root = os.path.dirname(os.path.abspath(sys.executable))
	
	# Lista de arquivos do DeltaTalk a serem removidos
	deltatalk_files = {
	"br*.dsp",
	"brazil*.*",
	"brport.lng",
	"Dtalk32T.dll",
	"dtdsp32t.dll",
	"prosody.dll",
	"serial.dll"
	}
	
	# Verifica se algum arquivo do DeltaTalk existe
	files_exist = any(os.path.isfile(os.path.join(nvda_root, f)) for f in deltatalk_files)
	if not files_exist:
		return  # Nada a fazer se os arquivos não estiverem presentes

	# Mensagem de confirmação
	result = gui.messageBox(
		"Os arquivos do DeltaTalk foram copiados para a pasta do NVDA durante a instalação (" + nvda_root + ").\n"
		"Deseja remover esses arquivos ao desinstalar o add-on?\n"
		"Nota: Apenas os arquivos específicos do DeltaTalk serão removidos.",
		"Confirmação de Desinstalação",
		wx.YES_NO | wx.ICON_QUESTION,
		gui.mainFrame
	)
	
	if result == wx.YES:
		try:
			for file_name in deltatalk_files:
				file_path = os.path.join(nvda_root, file_name)
				if os.path.isfile(file_path):
					os.remove(file_path)
					wx.MessageBox(
						f"Arquivo {file_name} removido com sucesso de {nvda_root}.",
						"Desinstalação Concluída",
						wx.OK | wx.ICON_INFORMATION
					)
		except Exception as e:
			wx.MessageBox(
				f"Erro ao remover arquivos: {e}\nAlguns arquivos podem permanecer em {nvda_root}.",
				"Erro",
				wx.OK | wx.ICON_ERROR
			)
			raise
	else:
		wx.MessageBox(
			"Os arquivos do DeltaTalk não serão removidos e permanecerão em " + nvda_root + ".",
			"Desinstalação Cancelada",
			wx.OK | wx.ICON_INFORMATION
		)