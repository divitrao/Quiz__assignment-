
console.log(data.user_answer)
console.log(data.correct_answer)

let correct_answer = data.correct_answer
let user_answer = data.user_answer

for(i=0;i<correct_answer.length;i++){
    if(correct_answer[i]['answer'].trim().toLowerCase() == user_answer[i]['textAnswer'].trim().toLowerCase()){
        $(`#result_${i+1}`).css({
                                    'background-color': '#a3f7b1',
                                    'border': '0.5px solid black'
        })
    }
    else{
        $(`#result_${i+1}`).css({
            'background-color': '#f7bea1',
            'border': '0.5px solid black'
})
    }
    
}