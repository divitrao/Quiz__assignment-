let params = (new URL(document.location)).searchParams
let subject = params.get('subject')

let exam_time = extra_data['alloted_time']  // this data is been dumped from view.py to game.html and from there it is collected via escape js function
let exam_number  = extra_data['exam_number']


$.ajax({
    url: `http://127.0.0.1:8000/api/${subject}/`,
    datatype : 'json',
    success : function(data){
            let question_number = 0
            let selected_option = []
            let minute
            let second
            let show_second

/*********************************************  TIMER FUNCTION *********************************************************/

            function timer(data,question_number){
                if(data[question_number]['progress'].length == 1){
                    minute = parseInt(data[question_number]['progress'][0]['minutes'])
                    second = parseInt(data[question_number]['progress'][0]['seconds'])
                    console.log(minute,second)
                }
                else{
                    minute = exam_time
                    second = 0
                }

                 let intervel = window.setInterval(function(){
                     console.log('hi')
                    if(second == 0 && minute == 0){
                        $('#submit').click()
                    }
                    else{
                        if(second == 0){
                            minute = minute - 1
                            second = 60
                        }
                        second = second - 1

                        if(second < 10){
                             show_second = '0' + String(second)
                        }
                        else{
                            show_second = String(second)
                        }

                        if(minute == 0){
                            $('#countdown').html(show_second + ' seconds')
                        }
                        else{
                            $('#countdown').html(minute + ':' + show_second)
                        }
                    }
                },1000)


                let question_id = data[question_number]['id']
                $(window).on('unload',function(){
                        
                        let cookie = document.cookie
                        let csrfToken = cookie.substring(cookie.indexOf('=')+1)
                        let form_data = new FormData()
                        form_data.append('csrfmiddlewaretoken', csrfToken)
                        form_data.append("minute", minute)
                        form_data.append("second",second)
                        form_data.append('subject',subject)
                        form_data.append('question_id',question_id)
                        navigator.sendBeacon('http://127.0.0.1:8000/play/updatetime/',form_data)  


                    
                })
                
            }

         /*********************************************  Question display  function *********************************************************/

            function display_question(question_number){
                
                 

                // getiing main div tag from html file
                let main_div_tag = document.getElementById('display_quiz')


                // creating a new div tag to have question and options all together

                let div_tag = document.createElement('div')
                div_tag.id = 'temporary_div'

                // creating template for question and option to display it to user
                    let question_div_tag = document.createElement('div')
                    question_div_tag.innerHTML = data[question_number]['question']

                    
                    question_div_tag.setAttribute('style','height:40px; text-align:center ; font-size:20px; margin-top:20px; padding:10px')
                   
                  
                // appending question to main div tag
                div_tag.appendChild(question_div_tag)

                // looping over the options of the related question if it is MCQ 
                if (data[question_number]['type'] == 'mcq'){
            
                    for(let i=0 ; i< data[question_number]['answers'].length ; i++){
                        
                        let parent_div = document.createElement('div')
                        parent_div.id = `option_${i}`
                        parent_div.setAttribute('style','height:70px; text-align:center ; font-size:20px; margin-top:2%; padding:10px; border: 1px solid black; align-items: center;margin-right:10%; margin-left:10%')


                        let option_div_tag = document.createElement('div')
                        option_div_tag.id = data[question_number]['answers'][i]['id']
                        option_div_tag.innerHTML = data[question_number]['answers'][i]['options']

                        parent_div.addEventListener('click', ()=>{
                            let this_id = parent_div.id
                            get_id(this_id)
                        
                        })
                        parent_div.appendChild(option_div_tag)
                        

                        // appending options div to main div tag
                        div_tag.appendChild(parent_div)
                    }
            
                }

                // creating a text input if question type is one word
                else{
                        let one_word_div_tag = document.createElement('div')
                        one_word_div_tag.setAttribute('style','height:40px; text-align:center ; font-size:20px; margin-top:20px; padding:10px')

                        let text_input_tag = document.createElement('input')
                        text_input_tag.type = 'text'
                        text_input_tag.id = 'one_word'
                        one_word_div_tag.appendChild(text_input_tag)
                        div_tag.appendChild(one_word_div_tag)
                }

                main_div_tag.appendChild(div_tag)
                
            }
            
    /*********************************************  calling display and timer fuction when page loaded *********************************************************/

            display_question(question_number)
            timer(data,question_number)

    /*********************************************  reloading page once user submits answer *********************************************************/
            $('#submit').click(function(){                                                                // onclick function to check answer 
                if(data[question_number]['type'] == 'mcq'){
                    check_answer_mcq(selected_option,question_number)
                }
                else{
                    let word = document.getElementById('one_word').value.trim().toLowerCase()
                    check_one_word(word,question_number)
                }
                
                
                // display_question(question_number)
                if(data.length == 1){
                    $('#submit').attr('href',`/play/result/${subject}/${exam_number}/`)
                    
                }
                
                
                $('#temporary_div').remove()
                location.reload()
            })


     /*********************************************  Checking one word answer *********************************************************/

            function check_one_word(word,question_number){                           // check one word answer function
                let is_correct 
                if(word == data[question_number]['answers'][0]['options']){
                    is_correct = true
                }
                else{
                    is_correct = false
                }



                //sending data to database to update user answer table
                let marks
                if(is_correct == true){
                    marks = data[question_number]['marks']
                }
                else{
                    marks = 0
                }
                let typed_word

                if(word.length==0){
                    typed_word = 'not attempted'
                }
                else{
                    typed_word = word
                }

                let cookie = document.cookie
                let csrfToken = cookie.substring(cookie.indexOf('=')+1)
                let form_data = new FormData()
                form_data.append('csrfmiddlewaretoken', csrfToken)
                form_data.append("question", data[question_number]['id'])
                form_data.append('text_answer',typed_word)
                form_data.append("marks",marks)
                form_data.append('is_correct',is_correct)
                form_data.append('exam_number',exam_number)
                navigator.sendBeacon('http://127.0.0.1:8000/play/update/',form_data)

            }


/*********************************************  checking MCQ answer *********************************************************/


            function  check_answer_mcq(selected_answer_id,question_number){                     // check mcq answer function 
                let is_correct
                let choosen_answer
                if(selected_answer_id.length!=0){
                    

                        for(let i=0 ; i<data[question_number]['answers'].length; i++){
                            
                            if(data[question_number]['answers'][i]['id']==selected_answer_id[0]){
                                
                                if(data[question_number]['answers'][i]['checkAnswerBool']==true){
                                    is_correct = true
                                    choosen_answer = data[question_number]['answers'][i]['options']
                                    break
                                }
                                else{
                                    is_correct = false
                                }

                                
                            }
                            else{
                                is_correct = false
                                continue
                            }
                            choosen_answer = data[question_number]['answers'][i]['options']
                        }
    
                    

                }else{
                    is_correct = false
                    choosen_answer = 'not attempted'
                }
                

                //sending data to database to update user answer table
                let marks
                if(is_correct == true){
                    marks = data[question_number]['marks']
                }
                else{
                    marks = 0
                }
                let cookie = document.cookie
                let csrfToken = cookie.substring(cookie.indexOf('=')+1)
                let form_data = new FormData()
                form_data.append('csrfmiddlewaretoken', csrfToken)
                form_data.append("question", data[question_number]['id'])
                form_data.append('text_answer',choosen_answer)
                form_data.append("marks",marks)
                form_data.append('is_correct',is_correct)
                form_data.append('exam_number',exam_number)
                navigator.sendBeacon('http://127.0.0.1:8000/play/update/',form_data)
                
            }

            
/*********************************************  Getting ID of selected option  *********************************************************/
            function get_id(elem_id){                                        // get id of the selected div function
                selected_option = []

                let child_id= document.getElementById(elem_id).children
                selected_option.push(child_id[0].id)
                change_background_color(elem_id)
                console.log(selected_option)
            }

    /*********************************************  changing background color once user changes option *********************************************************/        

            function change_background_color(elem_id){                             // change background color of div function
                console.log(elem_id,)
                for(let i=0 ; i<data[question_number]['answers'].length; i++){
                    if(elem_id == `option_${i}`){
                        $(`#${elem_id}`).css("background-color",'rgba(255,204,0)')
                    }
                    else{
                        $(`#option_${i}`).css("background-color",'white')
                    }
                }
            }

    /*********************************************  clearing option if user wants to unselect options  *********************************************************/

            $('#clear').click(function(){                                        // clear selected options function

                for(let i=0 ; i<data[question_number]['answers'].length; i++){
                    
                        selected_option = []
                        $(`#option_${i}`).css("background-color",'white')
                    
                }

            })


            
    }
})



