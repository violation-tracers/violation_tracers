def chaser(model_result):
    answer = [] 
    if 0 in model_result or 3 in model_result:
        if 5 in model_result:
            answer.append('차량 정지선 위반입니다.')
        elif 8 in model_result:
            if 11 not in model_result:
                answer.append('오토바이 정지선 위반 혹은 보행자 안전 위협 행위입니다.')
                answer.append('오토바이 헬멧 미착용입니다.')
            else: 
                answer.append('오토바이 정지선 위반 혹은 보행자 안전 위협행위입니다.')
    elif 10 in model_result:
        answer.append('보행자 안전 위협행위 혹은 오토바이 불법 주정차입니다')
    elif 7 in model_result :
        if 11 not in model_result:
            answer.append('오토바이 헬멧 미착용입니다.')
    elif 6 in model_result:
        answer.append('차량 중앙선 침범 혹은 갓길 불법 주정차입니다')
    elif 5 in model_result:
        if 0 not in  model_result or 1 not in model_result or 2 not in model_result or 3 not in model_result:
            answer.append('차량 불법 주정차입니다.')
    elif 8 in model_result or 9 in model_result:
        if 0 not in  model_result or 1 not in model_result or 2 not in model_result or 3 not in model_result:
            if 11 not in model_result:
                answer.append('오토바이 불법 주정차입니다')
                answer.append('오토바이 헬멧 미착용입니다.')
            else:
                answer.append('오토바이 불법 주정차입니다')
            
    else:
        answer.append('합법입니다.')
   
    return answer





