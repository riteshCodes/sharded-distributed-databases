from multiprocessing import Process
import client

if __name__ == "__main__":

    test_user_ids = []
    test_names = []
    test_emails = []
    for i in range(1000):
        test_user_ids.append(i)
        test_names.append(f'N-:{str(i)}')
        test_emails.append(f'@Email-:{str(i)}')

    COUNT = 1
    PROCESSES = {}
    for x in range(COUNT):
        PROCESSES[x] = Process(target=client.run(u_ids=test_user_ids, names=test_names, emails=test_emails))

    for x in range(COUNT):
        PROCESSES[x].start()
