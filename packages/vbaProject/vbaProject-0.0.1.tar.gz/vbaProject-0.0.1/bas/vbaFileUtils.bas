Attribute VB_Name = "vbaFileUtils"
Function getUserDesktop()
    ' 获取桌面路径
    Dim objShell As Object
    Set objShell = CreateObject("WScript.Shell")
    getUserDesktop = objShell.SpecialFolders("Desktop")
End Function

Function getFileNameFromPath(fullPath As String) As String
    ' 根据路径获取文件名
    If fullPath = "" Then
        getFileNameFromPath = ""
        Exit Function
    End If
    Dim arr() As String
    arr = Split(fullPath, "\")
    getFileNameFromPath = arr(UBound(arr))
End Function
Function getetDirectoryFromFilePath(filePath As String) As String
    ' 根据文件名获取路劲
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    getetDirectoryFromFilePath = fso.GetParentFolderName(filePath)
    Set fso = Nothing
End Function

Function IsDirectory(path As String) As Boolean
    ' 判断路径是否是文件夹
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
    ' 判断文件是否存在
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
    ' 列当前文件夹下指定后缀的文件
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
    ' 列出当前文件夹下所有CSV文件
    ListCSVFiles = ListFiles(strFolderPath, "csv")
End Function

Sub test()
    ' MsgBox getUserDesktop()
    Dim strFolderPath As String
    strFolderPath = "C:\Users\my117\Desktop" '请将此处替换为您要遍历的文件夹路径

    Dim csvFilePaths() As String
    csvFilePaths = ListCSVFiles(strFolderPath)
    
    Dim j As Integer
    For j = 0 To UBound(csvFilePaths) - 1
        MsgBox csvFilePaths(j)
    Next j
End Sub
