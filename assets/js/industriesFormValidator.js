
const industryValidator = ()=>{

    var industry_name = document.getElementById("industry_name");
    var ImageField1 = document.getElementById("ImageField1");
    var inner_heading = document.getElementById("inner_heading");
    var ImageField2 = document.getElementById("ImageField2");
    var caption = document.getElementById("caption");
    var description1 = document.getElementById("description1");
    var long_description = document.getElementById("long_description");

    if(industry_name.value == ""){
        showValidationError(industry_name,"Industry name is required");
    }
    else if(!ImageField1.value){
        showValidationError(ImageField1,"Image is required");
    }
    else if(!inner_heading.value){
        showValidationError(inner_heading,"Inner heading is required");
    }
    else if(!ImageField2.value){
        showValidationError(ImageField2,"Image is required");
    }
    else if(!caption.value){
        showValidationError(caption,"Caption is required");
    }
    else if(!description1.value){
        showValidationError(description1,"Description are required");
    }
    else if(!long_description.value){
        showValidationError(long_description,"Long description is required");
    }
    else{
        return true;
    }
    
}


const industryUpdateValidator = ()=>{

    var industry_name = document.getElementById("industry_name");
    var ImageField1 = document.getElementById("ImageField1");
    var inner_heading = document.getElementById("inner_heading");
    var ImageField2 = document.getElementById("ImageField2");
    var caption = document.getElementById("caption");
    var description1 = document.getElementById("description1");
    var long_description = document.getElementById("long_description");

    let update_image = ImageField1 ? ImageField1.getAttribute("data-value") || "" : "";
    let update_inner_image = ImageField2 ? ImageField2.getAttribute("data-value") || "" : "";

    if(industry_name.value == ""){
        showValidationError(industry_name,"Industry name is required");
    }
    else if(!ImageField1.value && !update_image.length>0){
        showValidationError(ImageField1,"Image is required");
    }
    else if(!inner_heading.value){
        showValidationError(inner_heading,"Inner heading is required");
    }
    else if(!ImageField2.value && !update_inner_image.length>0){
        showValidationError(ImageField2,"Image is required");
    }
    else if(!caption.value){
        showValidationError(caption,"Caption is required");
    }
    else if(!description1.value){
        showValidationError(description1,"Description are required");
    }
    else if(!long_description.value){
        showValidationError(long_description,"Long description is required");
    }
    else{
        return true;
    }
    
}