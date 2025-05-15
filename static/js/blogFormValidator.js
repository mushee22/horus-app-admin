
const blogValidator = ()=>{

    var heading = document.getElementById("heading");
    var image = document.getElementById("ImageField1");
    var inner_image = document.getElementById("ImageField2");
    var description1 = document.getElementById("description1");
    var long_description = document.getElementById("long_description");
    var industries = document.getElementById("industries");
    var customer = document.getElementById("customer");

    if(heading.value == ""){
        showValidationError(heading,"Heading is required");
    }
    else if(!image.value){
        showValidationError(image,"Image is required");
    }
    else if(!description1.value){
        showValidationError(description1,"Description is required");
    }
    else if(!inner_image.value){
        showValidationError(inner_image,"Inner image is required");
    }
    else if(!CKEDITOR.instances.long_description.getData()){
        showValidationError(long_description,"Long description is required");
    }
    else if(!industries.value){
        showValidationError(industries,"Industries are required");
    }
    else if(!customer.value){
        showValidationError(customer,"Customer is required");
    }
    else{
        return true;
    }
    
}


const blogUpdateValidator = ()=>{

    var heading = document.getElementById("heading");
    var image = document.getElementById("ImageField1");
    var inner_image = document.getElementById("ImageField2");
    var description1 = document.getElementById("description1");
    var long_description = document.getElementById("long_description");
    var industries = document.getElementById("industries");
    var customer = document.getElementById("customer");

    let update_image = image ? image.getAttribute("data-value") || "" : "";
    let update_inner_image = inner_image ? inner_image.getAttribute("data-value") || "" : "";

    if(heading.value == ""){
        showValidationError(heading,"Heading is required");
    }
    else if(!image.value && !update_image.length>0){
        showValidationError(image,"Image is required");
    }
    else if(!description1.value){
        showValidationError(description1,"Description is required");
    }
    else if(!inner_image.value && !update_inner_image.length>0){
        showValidationError(inner_image,"Inner image is required");
    }
    else if(!CKEDITOR.instances.long_description.getData()){
        showValidationError(long_description,"Long description is required");
    }
    else if(!industries.value){
        showValidationError(industries,"Industries are required");
    }
    else if(!customer.value){
        showValidationError(customer,"Customer is required");
    }
    else{
        return true;
    }
    
}