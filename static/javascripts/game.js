

$('#answer_submission').click(function(){
    window.localStorage.setItem(`submitted_${data['subject']}`, true)
})


starttime(data)



function starttime(data){
    let minute = data['minute']
    let second = data['second']
    let timer = 0
    let show_second
    // if(data['question_id']==localStorage.getItem(`questionId_${data['subject']}`) && data['user_id']==localStorage.userid && localStorage.getItem(`submitted_${data['subject']}`)=='false' ){
    //         timer = parseInt(localStorage.getItem(`timer_${data['subject']}`))
    //         minute = parseInt(localStorage.getItem(`minute_${data['subject']}`))
    //         second = parseInt(localStorage.getItem(`seconds_${data['subject']}`))
            


    // }
    // else{
    //     timer = 0 
    //     minute = parseInt(data['time'])-1
    //     second = 60

    // }





interval = window.setInterval(function(){
// if (timer==parseInt(data['minute'])*60-1){
     
//         document.getElementById('answer_submission').click()
        
//     }

if(second==0 && minute==0){
    document.getElementById('answer_submission').click()
}

else{
    
    
    if(second==0){
        minute = minute-1
        second = 60
    }
    second = second-1
    if(second<10){
        show_second = '0' + String(second)
    }
    else{
        show_second = String(second)
    }
    
    if(minute==0){
        $('#countdown').html(show_second +' seconds')

    }
    else{
        $('#countdown').html(minute+':'+show_second)
    }
    // window.localStorage.setItem(`timer_${data['subject']}`,timer)
    // window.localStorage.setItem(`questionId_${data['subject']}`,data['question_id'])
    // window.localStorage.setItem('userid',data['user_id'])
    // window.localStorage.setItem(`minute_${data['subject']}`, minute)
    // window.localStorage.setItem(`seconds_${data['subject']}`, second)
    // window.localStorage.setItem(`submitted_${data['subject']}`, false)

    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/quiz/timeupdate',
        data :{'minute':minute,
                'seconds':second,
                'subject': data['subject']
                },
        async : false
    })
    

}

},1000)
}




