;title�����Ӧ��ȷ�����ڵ�title,"text"��д�ɲ�д��
ControlFocus("��","","Edit1")
WinWait("[CLASS:#32770]","",10)
;ControlSetText("��","","Edit1","D:\upload_file.txt")  ����ġ�text�� ����д��д�Ͳ�����ȷִ����
ControlSetText("��","","Edit1",$CmdLine[1])
Sleep(2000)
ControlClick("��","","Button1")