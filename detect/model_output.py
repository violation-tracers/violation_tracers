def chaser(model_result):

    model_result = eval(model_result)

    answer = []

    for l in model_result:

        if l == 5:

            if 0 in model_result or 3 in model_result:
                answer.append('차량 정지선 위반입니다.')

            elif 1 in model_result or 2 in model_result:
                pass

            else:
                answer.append('차량 정지선 위반 혹은 차량 불법 주정차입니다.')

        if l == 6:

            answer.append('차량 중앙선 침범 혹은 차량 불법 주정차입니다.')

        if l == 7:
            if 11 not in model_result:
                answer.append('오토바이 헬멧 미착용입니다.')
            if 11 in model_result:
                pass

        if l == 8:

            if 11 not in model_result:
                answer.append('오토바이 헬멧 미착용입니다.')
            
                if 0 in model_result or 3 in model_result:
                    answer.append('오토바이 정지선 위반입니다.')
                    
                if 1 in model_result or 2 in model_result:
                    pass
                else:
                    answer.append('오토바이 정지선 위반 혹은 차량 불법 주정차입니다.')

            elif 11 in model_result:

                if 0 in model_result or 3 in model_result:
                    answer.append('오토바이 정지선 위반입니다.')
                    
                if 1 in model_result or 2 in model_result:
                    pass
                else:
                    answer.append('오토바이 정지선 위반 혹은 차량 불법 주정차입니다.')
        
        if l == 9:

            answer.append('오토바이 중앙선 침범 혹은 차량 불법 주정차입니다.')

        if l == 10:

            answer.append('보행자 안전 위협행위 혹은 오토바이 불법 주정차입니다')

        if l == 12:

            answer.append('보행자 안전 위협행위 혹은 차량 불법 주정차입니다.')
            
    if not answer:
        answer.append('위반사항을 찾을 수 없습니다.')


    answer = set(answer)     
    return answer       

