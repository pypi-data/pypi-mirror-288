from app_auth import get_access_token
import azure_utils


client_id = '3294359a-0012-4cab-868e-1bfb884f6e2c'
client_secret = '7-O8Q~xciH.vjcUDJuDyN55UGl~Yy6E.T6PXMb_l'
tenant_id = 'c187ee01-4e4e-40c8-b342-f82c8d699421'

token = get_access_token(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)

result_user_id = azure_utils.get_user_from_upn('teams.manager@angelcompany.com', access_token=token)
user_id = result_user_id.get('id')


#find_group = azure_utils.get_user_group_by_name(user_id, group_name='makemeadmin', access_token=token)

#group_name = find_group.get('group_name')
#group_id = find_group.get('group_id')



group_id_remove = '37d04d5d-6597-40f8-b988-8d83956b6ded'

#print (user_id)
#print(group_name)
#print(azure_utils.add_user_to_group('teams.manager@angelcompany.com', 'uninstall-makemeadmin', token))

#print(azure_utils.get_group_by_name('backoffice-01', token))

#print(azure_utils.get_user_group_by_name(user_id,'mm-allow-makemeadmin',token))

print(azure_utils.add_user_to_group('teams.manager@angelcompany.com','sdfsdfhgctgcsev',token))
#print(azure_utils.remove_user_from_group('teams.manager@angelcompany.com', 'mm-allow-makemeadmin', token))
#print(azure_utils.get_user_group_by_name(user_id,'mm-allow-makemeadmin',token))


'''
resp = {'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#groups(displayName,id)', '@odata.count': 10, 'value': [{'displayName': 'intune-grp-prod-mm-ferrosud-backoffice-01', 'id': '0176182f-b9e3-46e0-aa80-eea29242282a'}, {'displayName': 'intune-grp-prod-mm-ferrosud-backoffice-allow-usb-01', 'id': '0586b5c2-436f-44ad-9897-6219fe54f88d'}, {'displayName': 'intune-grp-prod-mm-backoffice-allow-usb-01', 'id': '07f26c97-828a-4279-b4a9-956e30638d0f'}, {'displayName': 'azure-grp-user-prod-mm-tv-backoffice-conditionalaccess-allow-italy-01', 'id': '24d26a18-53c5-4b60-9ed3-d7ef6f9fecfe'}, {'displayName': 'intune-grp-prod-mmste-backoffice-allow-usb-01', 'id': '9cf4c77c-ff8e-4b3c-aeb7-8be845c4d1b3'}, {'displayName': 'azure-grp-user-prod-mm-tv-backoffice-conditionalaccess-allow-global-01', 'id': 'b02658ab-3988-458e-8b29-2f8de29d8200'}, {'displayName': 'intune-grp-prod-mmste-backoffice-01', 'id': 'de46fcab-3df1-4872-a185-9019c68cbeb2'}, {'displayName': 'azure-grp-user-prod-mm-tv-backoffice-conditionalaccess-allow-europe-01', 'id': 'df6deb3b-0427-4075-a833-719e8905ef7b'}, {'displayName': 'intune-grp-prod-mm-backoffice-01', 'id': 'f0206d30-f281-4e66-bfeb-82b3a095703a'}, {'displayName': 'intune-grp-prod-mmste-backoffice-office32bit-01', 'id': 'feef7f05-054d-40d1-8c0b-ac56e740b37f'}]}    
groups_data = resp.json()
print(resp)
'''