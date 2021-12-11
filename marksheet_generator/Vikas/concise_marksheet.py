def concise_marksheet_generator():
    import os
    import csv
    os.system('cls')
    if not os.path.exists(r"Vikas/marksheets/"):
        os.mkdir('Vikas\\marksheets')
    master_path = r'media/master_roll.csv'
    responses_path = r'media/responses.csv'
    if not os.path.exists(master_path):
        print('ERROR')
        return
    if not os.path.exists(responses_path):
        print('ERROR')
        return
    master_dict = {}
    with open(master_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != 'roll':
                master_dict[row[0]] = row[1]

    responses_dict = {}
    with open(responses_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[6] != 'Roll Number':
                responses_dict[(row[6]).upper()] = [
                    row[0], row[1], row[2], row[3], row[4], row[5], row[7:]]

    if 'ANSWER' in responses_dict.keys():
        answer_key = responses_dict['ANSWER'][6]
    else:
        print('no roll number with ANSWER is present, Cannot Process!')
        return
    # print(answer_key)

    total_ques = len(answer_key)

    if not os.path.exists('Vikas/marks.csv'):
        correct_marks = 5
        wrong_marks = -1
    with open('Vikas/marks.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            correct_marks = float(row[0])
            wrong_marks = float(row[1])
            break

    score = {}
    header_for_answers = []
    for i in range(total_ques):
        header_for_answers.append('Unnamed: '+str(7+i))
    header = ['Timestamp', 'Email address', 'Google_Score', 'Name', 'IITP webmail',
              'Phone (10 digit only)', 'Score_After_Negative', 'Roll Number']
    header.extend(header_for_answers)
    header.append('statusAns')
    # j = 0
    for key, value in master_dict.items():
        right = 0
        wrong = 0
        if key not in responses_dict.keys():
            # print('absent')
            concise_info = ['', '', 'ABSENT',
                            master_dict[key], '', '', 'ABSENT', key]
            if os.path.exists('Vikas/marksheets/concise_marksheet.csv'):
                with open('Vikas/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(concise_info)
                    file.close()
            else:
                with open('Vikas/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(header)
                    writer.writerow(concise_info)
                    file.close()

        else:
            for i in range(total_ques):
                if responses_dict[key][6][i] == answer_key[i]:
                    right += 1
                elif len(responses_dict[key][6][i]) != 0:
                    wrong += 1
        not_attempted = total_ques-right-wrong
        score[key] = [right, wrong, not_attempted]
        final_marks = correct_marks*right + wrong_marks*wrong
        Score_After_Negative = str(final_marks) + \
            '/' + str(total_ques*correct_marks)
        concise_info = [responses_dict[key][0], responses_dict[key][1],
                        responses_dict[key][2], responses_dict[key][3], responses_dict[key][4], responses_dict[key][5], Score_After_Negative, key]
        concise_info.extend(responses_dict[key][-1])
        concise_info.append(score[key])
        if os.path.exists('Vikas/marksheets/concise_marksheet.csv'):
            with open('Vikas/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                # f.write(concise_info)
                writer = csv.writer(file)
                writer.writerow(concise_info)
                file.close()
        else:
            with open('Vikas/marksheets/concise_marksheet.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerow(concise_info)
                file.close()
        # j += 1
        # if j == 10:
        #     break


# concise_marksheet_generator()
