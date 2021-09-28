
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/api/',
        datatype: "json",
        success: function(data){
            
            console.log(data)
            for(i=0;i<data.length;i++){
                let main_div = document.createElement('div')
                main_div.className = ' col-md-4'
                main_div.title= `you have ${data[i]['alloted_time']} minutes for each question`

                //creating  'a' tag 
                let a_tag = document.createElement('a')
                a_tag.className = 'text-dark'
                a_tag.href = `/play/start?subject=${data[i]['slug']}`

                //creating card as in bootstarp 
                let div_one = document.createElement('div')
                div_one.className = 'card mb-4 box-shadow'

                let div_two = document.createElement('div')
                div_two.className = 'card-body text-center'

                let div_three = document.createElement('div')
                div_three.className = 'd-flex justify-content-around align-items-center text-center'

                //creating small tag to display subject name
                let small_tag = document.createElement('small')
                small_tag.className = 'font-weight-bold'
                small_tag.innerHTML = data[i]['quiz_description']

                //appending all tags to its parent tag

                div_three.appendChild(small_tag)
                div_two.appendChild(div_three)
                div_one.appendChild(div_two)
                a_tag.appendChild(div_one)
                main_div.appendChild(a_tag)

                let card_footer = document.createElement('div')
                card_footer.className = 'card-footer d-flex justify-content-between'
                let right_div = document.createElement('div')
                right_div.innerHTML = 'right'
                let left_div = document.createElement('div')
                left_div.innerHTML = 'left'
                card_footer.appendChild(left_div)
                card_footer.appendChild(right_div)
               

                main_div.appendChild(card_footer)


                //now lastly appending it to main parent tag in html 

                let main_parent = document.getElementById('display_list')
                main_parent.appendChild(main_div)


            }
           
        }
    })




