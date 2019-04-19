while($true){
(get-netconnectionProfile).Name | Out-File -filepath Resources/Temporary_files/Current_Network.txt
Start-Sleep -s 5
}