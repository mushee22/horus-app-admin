

let popUp = document.querySelector(".popup-bg");

//show delete pop up
const showDeletePopup = (id,name)=>{
    popUp.classList.remove('popup-hide');
    popUp.querySelector('.pop-up-delete').classList.remove('popup-hide');
    popUp.querySelector('input[name="delete_id"]').value = id;
    popUp.querySelector(".delete-item").innerHTML = name;
}



//show request reject pop up
const showRejectPopup = (id,code)=>{
    popUp.classList.remove('popup-hide');
    popUp.querySelector('.pop-up-reject').classList.remove('popup-hide');
    popUp.querySelector('input[name="reject_id"]').value = id;
    popUp.querySelector(".reject-item").innerHTML = code;
}


//show request complete pop up
const showCompletePopup = (id,code)=>{
    popUp.classList.remove('popup-hide');
    popUp.querySelector('.pop-up-complete').classList.remove('popup-hide');
    popUp.querySelector('input[name="complete_id"]').value = id;
    popUp.querySelector(".complete-item").innerHTML = code;
}



//show employee assign pop up
const  showAssignPopup  = async (id,category)=>{
    popUp.classList.remove('popup-hide');
    popUp.querySelector('.pop-up-assign').classList.remove('popup-hide');
    let labourSelect = document.getElementById('labourSelect');
    while(labourSelect.options.length>0){
        labourSelect.options[0].remove()
    }
    let reqId = document.getElementById("reqId");
    reqId.value = id;
    await fetch(`/labours/active?category=${category}`,{
        'method':'GET'
    }).then(resp=>resp.json()).then(data=>{
        if(data.resp_code==1){
            if(data.data.length > 0){
                data.data.forEach(obj=>{
                    var option = document.createElement('option')
                    option.innerHTML = obj.first_name + " " + obj.last_name;
                    option.value = obj.id;
                    labourSelect.append(option);
                });
            }
            else{
                var option = document.createElement('option')
                option.innerHTML = "No labours are created for this category"
                option.value = "";
                labourSelect.append(option);
            }
            
        }
    });
}

// hide pop ups
const hidePopup = (e)=>{
    e.closest('.pop-up').classList.add('popup-hide')
    popUp.classList.add('popup-hide');
}