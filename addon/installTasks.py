import os
import sys
import shutil
import gui
import wx
import subprocess

def onInstall():
	# Caminho do add-on
	addon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "synthDrivers", "deltatalk")
	# Caminho do NVDA (raiz onde está nvda.exe)
	nvda_root = os.path.dirname(os.path.abspath(sys.executable))
	target_path = nvda_root

	# Mensagem de confirmação
	result = gui.messageBox(
		"Este add-on requer que os arquivos do DeltaTalk sejam copiados para a pasta do programa NVDA (" + target_path + ").\n"
		"Se os arquivos não forem copiados, a DLL do DeltaTalk não os detectará e não será inicializada corretamente, impedindo o funcionamento do sintetizador.\n"
		"Deseja copiar agora os arquivos do DeltaTalk para a pasta do programa NVDA? Nota: A cópia dos arquivos pode não ser bem-sucedida se o NVDA não estiver sendo executado como administrador.",
		"Confirmação de Instalação",
		wx.YES_NO | wx.ICON_QUESTION,
		gui.mainFrame
	)
	if result == wx.YES:
		try:
			# Copia arquivos diretamente para a raiz do NVDA
			for item in os.listdir(addon_path):
				source = os.path.join(addon_path, item)
				destination = os.path.join(target_path, item)
				if os.path.isfile(source):
					try:
						shutil.copy2(source, destination)
					except PermissionError:
						# Tenta copiar com elevação
						cmd = f'cmd.exe /c copy "{source}" "{destination}"'
						subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
						gui.messageBox(
							"Permissões elevadas foram necessárias para copiar os arquivos.",
							"Informação",
							wx.OK | wx.ICON_INFORMATION,
							gui.mainFrame
						)
			gui.messageBox(
				"Arquivos DeltaTalk copiados com sucesso para:\n" + target_path,
				"Instalação Concluída",
				wx.OK | wx.ICON_INFORMATION,
				gui.mainFrame
			)
		except Exception as e:
			gui.messageBox(
				f"Erro ao copiar arquivos: {e}\nA instalação será cancelada.",
				"Erro",
				wx.OK | wx.ICON_ERROR,
				gui.mainFrame
			)
			raise
	else:
		gui.messageBox(
			"Instalação cancelada pelo utilizador.",
			"Instalação Cancelada",
			wx.OK | wx.ICON_INFORMATION,
			gui.mainFrame
		)
		raise Exception("Instalação cancelada pelo utilizador")