import numpy as np

security_whitelist = [
    'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'e', 'exp', 'log', 'log10', 'log2', 'abs', 'pi', 'sqrt'
]

divider_list = ['_', '+', '-', '*', '/', '^',  '(', ')', "'", '"', '.', ',', '[', ']', ';', ':', '%']


def is_checked_valid(cmd):
    is_valid = True
    has_cutted = False
    start_index = end_index = 0
    while cmd[start_index] in divider_list:
        start_index += 1
        end_index += 1
    while end_index + 1 < len(cmd):
        end_index += 1
        if cmd[end_index] in divider_list:
            cut_cmd = cmd[start_index:end_index]
            has_cutted = True
            # print(cut_cmd, start_index, end_index)
            if not (cut_cmd in security_whitelist or cut_cmd.isdigit()):
                is_valid = False
                break
            start_index = end_index + 1
            while start_index < len(cmd) and cmd[start_index] in divider_list:
                start_index += 1
                if start_index >= len(cmd):
                    start_index = end_index = len(cmd)
                    break
            end_index = start_index
    if has_cutted:
        return is_valid
    else:
        return cmd in security_whitelist


def pre_process(funString):
    """Convert the standard function expression into numpy form
        E.g. input  = 'arcsin(exp(a*x)^2)'
             output = 'np.arcsin(np.power(np.exp(a*x), 2))'
        """
    if not is_checked_valid(funString):
        return "Invalid operation!"

    tempString = funString
    for item in security_whitelist:
        need_brackets = False
        if item in ['e', 'pi']:
            need_brackets = True
        index_t = 0
        while index_t < len(tempString):
            index_t_l = tempString.find(item, index_t)
            if index_t_l == -1:
                break
            index_t_r = index_t_l +len(item)
            if (index_t_r < len(tempString) and not tempString[index_t_r].isalpha() and not tempString[index_t_r].isdigit()):
                if index_t_l == 0 or (not tempString[index_t_l-1].isalpha() and not tempString[index_t_l-1].isdigit()):
                    tempString = tempString[:index_t_l] + '{}np.{}{}'.format('(' if need_brackets else '', item, ')' if need_brackets else '') + tempString[index_t_r:]
                    index_t = index_t_l + len('np.' + item) + (2 if need_brackets else 0)
                else:
                    break
            elif index_t_r >= len(tempString):
                tempString = tempString[:index_t_l] + '{}np.'.format('(' if need_brackets else '') + tempString[index_t_l:] + ')' if need_brackets else ''
                index_t = index_t_l + len('np.' + item) + (2 if need_brackets else 0)
            else:
                index_t += 1
                continue
    index = 0
    while index < len(tempString):
        index = tempString.find('^', index)
        if index == -1:
            break
        index_l = index - 1
        count_bracket = 0
        while tempString[index_l] == ' ':
            index_l -= 1
        if tempString[index_l].isalpha() or tempString[index_l].isdigit():
            while index_l >= 0:
                index_l -= 1
                if not tempString[index_l].isalpha() and not tempString[index_l].isdigit():
                    break
        elif tempString[index_l] == ')':
            count_bracket += 1
            while index_l >= 0:
                index_l -= 1
                if tempString[index_l] == ')':
                    count_bracket += 1
                elif tempString[index_l] == '(':
                    count_bracket -= 1
                if count_bracket == 0:
                    index_l -= 1
                    if not tempString[index_l].isalpha() and not tempString[index_l].isdigit():
                        break
                    else:
                        index_l -= 1
                        while tempString[index_l].isalpha() or tempString[index_l].isdigit() or tempString[index_l] == '.':
                            index_l -= 1
                        break
        index_l += 1
        if index_l < 0:
            index_l = 0

        index_r = index + len('^')
        count_bracket = 0
        while tempString[index_r] == ' ':
            index_r += 1
        if tempString[index_r].isalpha() or tempString[index_r].isdigit():
            while index_r < len(tempString) - 1:
                index_r += 1
                if not tempString[index_r].isalpha() and not tempString[index_r].isdigit():
                    break
        elif tempString[index_r] == '(':
            count_bracket += 1
            while index_r < len(tempString) - 1:
                index_r += 1
                if tempString[index_r] == '(':
                    count_bracket += 1
                elif tempString[index_r] == ')':
                    count_bracket -= 1
                if count_bracket == 0:
                    break
        index += 1
        if index_r < len(tempString) - 1:
            tempString = tempString.replace(tempString[index_l:index_r], 'np.power({}, {})'.format(tempString[index_l:index - 1], tempString[index:index_r]))
        else:
            tempString = tempString.replace(tempString[index_l:], 'np.power({}, {})'.format(tempString[index_l:index - 1], tempString[index:]))
    return tempString


pre_process_vector = np.vectorize(pre_process)
is_checked_valid = np.vectorize(is_checked_valid)


if __name__ == '__main__':
    print(pre_process_vector(['arcsin(exp(e*3)^2)', '3*log2(4)^(5*6)+(e-exp(abs(arctan(6*1)^e))/7^e', 'exp(e)', 'e^2', 'sin(pi^e)',
                              "__import__('os').system('ls')", 'a^x', 'import']))
    print(np.power(2, 7))
