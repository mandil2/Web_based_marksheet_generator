
def marksheet_generator():
    import os
    import csv
    import xlsxwriter as xlw
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
    with open(master_path,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != 'roll':
                master_dict[row[0]] = row[1]

    responses_dict = {}
    with open(responses_path,'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[6] != 'Roll Number':
                responses_dict[(row[6]).upper()] = [row[1], row[4], row[7:]]

    if 'ANSWER' in responses_dict.keys():
        answer_key = responses_dict['ANSWER'][2]
    else:
        print('no roll number with ANSWER is present, Cannot Process!')
        return
    # print(answer_key)

    total_ques = len(answer_key)
    # print(total_ques)
    score = {}
    for key, value in master_dict.items():
        right = 0
        wrong = 0
        if key not in responses_dict.keys():
            # print('absent')
            pass
        else:
            for i in range(total_ques):
                if responses_dict[key][2][i] == answer_key[i]:
                    right += 1
                elif len(responses_dict[key][2][i]) != 0:
                    wrong += 1
        not_attempted = total_ques-right-wrong
        score[key] = [right, wrong, not_attempted]
    # print(score['1401CB01'])
    if not os.path.exists('Vikas/marks.csv'):
        correct_marks = 5
        wrong_marks = -1
    with open('Vikas/marks.csv','r') as file:
        reader=csv.reader(file)
        for row in reader:
            correct_marks = float(row[0])
            wrong_marks = float(row[1])
            break
    
    # j = 0
    for key, value in master_dict.items():
        sheet_path = 'Vikas\\marksheets\\'+key+'.xlsx'
        workbook = xlw.Workbook(sheet_path)
        worksheet = workbook.add_worksheet('quiz')
        worksheet.set_column('A:E', 17)
        worksheet.insert_image('A1', 'Vikas/iit_patna_logo.png', {
            'x_scale': 0.85, 'y_scale': 0.82})
        merge_format = workbook.add_format({
            'bold': 1,
            'align': 'center',
            'fg_color': 'white',
            'font_size': 20,
            'underline': True,
            'font': 'Century',
            'border': 1})
        worksheet.merge_range('A5:E5', 'Mark Sheet', merge_format)
        name_format = workbook.add_format(
            {'font_size': 12, 'align': 'right', 'font': 'Century'})
        nameRoll_format = workbook.add_format(
            {'font_size': 12, 'align': 'left', 'font': 'Century', 'bold': 1})
        worksheet.write(
            'A6', 'Name:', name_format)
        worksheet.write(
            'B6', value, nameRoll_format)
        worksheet.write(
            'D6', 'Exam:', name_format)
        worksheet.write(
            'E6', 'quiz', nameRoll_format)
        worksheet.write(
            'A7', 'Roll Number:', name_format)
        worksheet.write(
            'B7', key, nameRoll_format)

        bold_format = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'font': 'Century', 'bold': 1, 'border': 1})
        worksheet.write('B9', 'Right', bold_format)
        worksheet.write('C9', 'Wrong', bold_format)
        worksheet.write('D9', 'Not Attempt', bold_format)
        worksheet.write('E9', 'Max', bold_format)
        worksheet.write('A10', 'No.', bold_format)
        worksheet.write('A11', 'Marking', bold_format)
        worksheet.write('A12', 'Total', bold_format)

        red_format = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'font': 'Century', 'color': 'red', 'border': 1})
        green_format = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'font': 'Century', 'color': 'green', 'border': 1})
        blue_format = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'font': 'Century', 'color': 'blue', 'border': 1})
        black_format = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'font': 'Century', 'border': 1})

        worksheet.write('A9','', black_format)
        worksheet.write('B10', score[key][0], green_format)
        worksheet.write('B11', correct_marks, green_format)
        worksheet.write('B12', correct_marks*score[key][0], green_format)

        worksheet.write('C10', score[key][1], red_format)
        worksheet.write('C11', wrong_marks, red_format)
        worksheet.write('C12', wrong_marks*score[key][1], red_format)

        worksheet.write('D10', score[key][2], black_format)
        worksheet.write('D11', 0, black_format)
        worksheet.write('D12','',black_format)
        worksheet.write('E10', total_ques, black_format)
        worksheet.write('E11','',black_format)

        total_marks = str(
            correct_marks*score[key][0]+wrong_marks*score[key][1])+'/'+str(total_ques*correct_marks)
        worksheet.write('E12', total_marks, blue_format)

        worksheet.write('A15', 'Student Ans', bold_format)
        worksheet.write('B15', 'Correct Ans', bold_format)

        if key not in responses_dict:
            # print('absent')
            row = 16
            for i in range(total_ques):
                correct_ans = 'B'+str(row)
                worksheet.write(correct_ans, answer_key[i], blue_format)
                row += 1
        else:
            row = 16
            for i in range(total_ques):
                student_ans = 'A'+str(row)
                correct_ans = 'B'+str(row)
                if responses_dict[key][2][i] == answer_key[i]:
                    worksheet.write(
                        student_ans, responses_dict[key][2][i], green_format)
                    worksheet.write(correct_ans, answer_key[i], blue_format)
                    row += 1
                elif len(responses_dict[key][2][i]) != 0:
                    worksheet.write(
                        student_ans, responses_dict[key][2][i], red_format)
                    worksheet.write(correct_ans, answer_key[i], blue_format)
                    row += 1
                else:
                    worksheet.write(
                        student_ans,'', black_format)
                    worksheet.write(correct_ans, answer_key[i], blue_format)
                    row += 1

        workbook.close()
        # j += 1
        # if j == 10:
        #     break
