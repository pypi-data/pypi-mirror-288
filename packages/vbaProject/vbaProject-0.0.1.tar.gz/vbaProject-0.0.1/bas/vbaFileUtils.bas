Attribute VB_Name = "vbaFileUtils"
Function getUserDesktop()
    ' ��ȡ����·��
    Dim objShell As Object
    Set objShell = CreateObject("WScript.Shell")
    getUserDesktop = objShell.SpecialFolders("Desktop")
End Function

Function getFileNameFromPath(fullPath As String) As String
    ' ����·����ȡ�ļ���
    If fullPath = "" Then
        getFileNameFromPath = ""
        Exit Function
    End If
    Dim arr() As String
    arr = Split(fullPath, "\")
    getFileNameFromPath = arr(UBound(arr))
End Function
Function getetDirectoryFromFilePath(filePath As String) As String
    ' �����ļ�����ȡ·��
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    getetDirectoryFromFilePath = fso.GetParentFolderName(filePath)
    Set fso = Nothing
End Function

Function IsDirectory(path As String) As Boolean
    ' �ж�·���Ƿ����ļ���
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    If fso.FolderExists(path) Then
        IsDirectory = True
    Else
        IsDirectory = False
    End If
    Set fso = Nothing
End Function
Function IsFile(filePath As String) As Boolean
    ' �ж��ļ��Ƿ����
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    If fso.FileExists(filePath) Then
        IsFile = True
    Else
        IsFile = False
    End If
    Set fso = Nothing
End Function



Function ListFiles(ByVal strFolderPath As String, ByVal suffix As String) As String()
    ' �е�ǰ�ļ�����ָ����׺���ļ�
    Dim objFSO As Object
    Set objFSO = CreateObject("Scripting.FileSystemObject")

    Dim objFolder As Object
    Set objFolder = objFSO.GetFolder(strFolderPath)

    Dim csvFiles() As String
    Dim i As Integer
    i = 0
    
    Dim hasFile As Boolean
    hasFile = False

    Dim objFile As Object
    For Each objFile In objFolder.Files
        If Right(objFile.Name, 4) = "." & suffix Then
            hasFile = True
            ReDim Preserve csvFiles(i)
            csvFiles(i) = objFile.path
            Debug.Print (objFile.path)
            i = i + 1
        End If
    Next objFile
    If hasFile Then
        ListFiles = csvFiles
    Else
        ReDim csvFiles(-1 To -1) As String
        ListFiles = csvFiles
    End If
    
End Function

Function ListCSVFiles(ByVal strFolderPath As String) As String()
    ' �г���ǰ�ļ���������CSV�ļ�
    ListCSVFiles = ListFiles(strFolderPath, "csv")
End Function

Sub test()
    ' MsgBox getUserDesktop()
    Dim strFolderPath As String
    strFolderPath = "C:\Users\my117\Desktop" '�뽫�˴��滻Ϊ��Ҫ�������ļ���·��

    Dim csvFilePaths() As String
    csvFilePaths = ListCSVFiles(strFolderPath)
    
    Dim j As Integer
    For j = 0 To UBound(csvFilePaths) - 1
        MsgBox csvFilePaths(j)
    Next j
End Sub
