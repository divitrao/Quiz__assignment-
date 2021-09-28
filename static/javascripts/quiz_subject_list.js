
    $.ajax({
        type: 'GET',
        url: 'http://127.0.0.1:8000/api/',
        datatype: "json",
        success: function(data){
            
            console.log(data)
            for(i=0;i<data.length;i++){
                let main_div = document.createElement('div')
                main_div.className = 'card card-custom gutter-b p-3 mr-3'
                let div_header = document.createElement('div')
                div_header.className = 'card-header'
                let div_title = document.createElement('div')
                div_title.className = 'card-title'
                let h_label = document.createElement('h3')
                h_label.className = 'card-label'
                h_label.innerHTML = 'histry'
                div_title.appendChild(h_label)
                div_header.appendChild(div_title)
                main_div.appendChild(div_header) 
                let div_body = document.createElement('div')
                div_body.innerHTML = 'lerem ipsum'
                main_div.appendChild(div_body)



                //now lastly appending it to main parent tag in html 

                let main_parent = document.getElementById('display_list')
                main_parent.appendChild(main_div)


            }
           
        }
    })




