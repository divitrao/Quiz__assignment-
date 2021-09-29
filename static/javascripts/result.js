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

        let elem_table = document.createElement('table')
        elem_table.className = 'table'
        elem_table.innerHTML = `<thead>
                                    <tr>
                                        <th scope='col'> Question </th>
                                        <th scope='col'> Your Answer </th>
                                        <th scope='col'> Correct Answer </th>
                                        <th scope='col'> Status </th>
                                    </tr>
                                </thead> `
        let elem_table_body = document.createElement('tbody')
        elem_table.appendChild(elem_table_body)

        
        for(i=0;i<data.length;i++){
            let user_answer = data[i]['user_answer'].trim().toLowerCase()
            let correct_answer = data[i]['correct_answer'].trim().toLowerCase()
            let row_color
            let result_status
            if(user_answer == correct_answer){
                marks = 5
                row_color = 'table-success'
                result_status = 'Correct'
                
            }
            else{
                marks = 0
                row_color = 'table-danger'
                result_status = 'Wrong'
                
            }

            let table_row = document.createElement('tr')
            table_row.className = `${row_color}`

            table_row.innerHTML = `<th> ${data[i]['question_text']} </th>
                                    <td> ${data[i]['user_answer']} </td>
                                    <td> ${data[i]['correct_answer']} </td>
                                    <td> ${result_status} </td>`

            elem_table_body.appendChild(table_row)

                div_tag.appendChild(elem_table)
                
        }

    }
})