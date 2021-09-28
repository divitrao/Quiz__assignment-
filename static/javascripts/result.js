console.log(extra_data)

let subject = extra_data['subject']
let exam_number = extra_data['exam_number']
let total_result_page = parseInt(extra_data['total_result'])


let result_page_number = parseInt(exam_number)



$('#previous,#next').click(function(){ 
    
    if(result_page_number>1){
        $("#previous").attr("href",`http://127.0.0.1:8000/play/result/${subject}/${result_page_number-1}/`)
    }
    if(result_page_number<total_result_page){
        $("#next").attr("href",`http://127.0.0.1:8000/play/result/${subject}/${result_page_number+1}/`)
    }
    
})

$.ajax({
    type:'GET',
    url:`http://127.0.0.1:8000/api/${subject}/${exam_number}/`,
    datatype:'json',
    success: function(data){
        let div_tag = document.getElementById('result_table')
        console.log(data)
        if(data.length == 0){
            let test_not_given_div = document.createElement('div')
            test_not_given_div.innerHTML = `<h1> TEST NOT GIVEN YET </h1>`
            test_not_given_div.className = 'text-center'
            div_tag.appendChild(test_not_given_div)
        }
        
        let marks 
        
        for(i=0;i<data.length;i++){
            let user_answer = data[i]['user_answer'].trim().toLowerCase()
            let correct_answer = data[i]['correct_answer'].trim().toLowerCase()
            
            let main_div = document.createElement('div')
            main_div.id = 'main_div'
            main_div.className = 'd-flex flex-column justify-content-center mb-2 mr-5 ml-5'

            let question_div = document.createElement('div')
            question_div.innerHTML = `<h2>${data[i]['question_text']}</h2>`
            question_div.className = 'mb-1 mt-1 p-2 text-center'
            main_div.appendChild(question_div)

            let user_answer_div = document.createElement('div')
            user_answer_div.innerHTML = `<h3>Your Answer :   ${data[i]['user_answer']}</h3>`
            user_answer_div.className = 'text-center'
            main_div.appendChild(user_answer_div)

            let correct_answer_div = document.createElement('div')
            correct_answer_div.innerHTML =  `<h3>Correct Answer : ' ${data[i]['correct_answer']}</h3>`
            correct_answer_div.className = 'text-center'
            main_div.appendChild(correct_answer_div)

            

            if(user_answer == correct_answer){
                marks = 5
                main_div.style.backgroundColor = "#91f57a"
            }
            else{
                marks = 0
                main_div.style.backgroundColor = "#f5655b"
            }

                div_tag.appendChild(main_div)
                
        }

    }
})