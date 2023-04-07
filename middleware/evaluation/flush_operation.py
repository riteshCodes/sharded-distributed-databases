from main import MWare

if __name__ == '__main__':
    m_ware = MWare()
    m_ware.flush_all()
    print(m_ware.key_space_inf())
    """
    u_ids = []
    names = []
    emails = []
    for i in range(1000):
        u_ids.append(i)
        names.append(f'N-:{str(i)}')
        emails.append(f'@Email-:{str(i)}')

    data = {'userID': u_ids, 'name': names, 'email': emails}
    m_ware.set_multiples(key_list=data['userID'], name_list=data['name'], email_list=data['email'])
    print(m_ware.key_space_inf())
    """