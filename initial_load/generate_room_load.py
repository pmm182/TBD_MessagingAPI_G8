from random import sample

if __name__ == '__main__':
    user_amount = 300
    room_amount = 600
    people_distribution = {2: 0.5, 3: 0.1, 5: 0.2, 10: 0.2}
    with open('users.txt', 'w') as f:
        for i in range(user_amount):
            f.write(f'user{i}\n')
    with open('rooms.txt', 'w') as f:
        for amount_of_people, percentage in people_distribution.items():
            amount_of_rooms = int(percentage * room_amount)
            inserted_groups = []
            for __ in range(amount_of_rooms):
                inserted = False
                while not inserted:
                    people = {f'user{id_}' for id_ in sample(range(user_amount), amount_of_people)}
                    if people not in inserted_groups:
                        inserted_groups.append(people)
                        inserted = True
                        f.write(','.join(people))
                        f.write('\n')

