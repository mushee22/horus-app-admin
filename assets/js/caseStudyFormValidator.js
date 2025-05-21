
const caseStudyValidator = ()=>{

    var heading = document.getElementById("heading");
    var image = document.getElementById("image");
    var inner_image = document.getElementById("inner_image");
    var client_overview = document.getElementById("client_overview");
    var client_says = document.getElementById("client_says");
    var challenge_description = document.getElementById("challenge_description");
    var solution_description = document.getElementById("solution_description");
    var result_description = document.getElementById("result_description");
    var industries = document.getElementById("industries");
    var country = document.getElementById("country");

    if(heading.value == ""){
        showValidationError(heading,"Heading is required");
    }
    // else if(!alphabetRegex.test(firstName.value)){
    //     showValidationError(firstName,"Numbers are not allowed in first name");
    // }
    else if(!image.value){
        showValidationError(image,"Image is required");
    }
    else if(!inner_image.value){
        showValidationError(inner_image,"Inner image is required");
    }
    else if(!client_overview.value){
        showValidationError(client_overview,"Client overview is required");
    }
    else if(!client_says.value){
        showValidationError(client_says,"Voice of Success is required");
    }
    else if(!challenge_description.value){
        showValidationError(challenge_description,"Challenge description is required");
    }
    else if(!solution_description.value){
        showValidationError(solution_description,"Solution description is required");
    }
    else if(!result_description.value){
        showValidationError(result_description,"Result description is required");
    }
    else if(!industries.value){
        showValidationError(industries,"Industries are required");
    }
    else if(!country.value){
        showValidationError(country,"Country is required");
    }
    else{
        return true;
    }
    
}


const caseStudyUpdateValidator = ()=>{

    var heading = document.getElementById("heading");
    var image = document.getElementById("image");
    var inner_image = document.getElementById("inner_image");
    var client_overview = document.getElementById("client_overview");
    var client_says = document.getElementById("client_says");
    var challenge_description = document.getElementById("challenge_description");
    var solution_description = document.getElementById("solution_description");
    var result_description = document.getElementById("result_description");
    var industries = document.getElementById("industries");
    var country = document.getElementById("country");

    let update_image = image ? image.getAttribute("data-value") || "" : "";
    let update_inner_image = inner_image ? inner_image.getAttribute("data-value") || "" : "";

    if(heading.value == ""){
        showValidationError(heading,"Heading is required");
    }
    else if(!image.value && !update_image.length>0){
        showValidationError(image,"Image is required");
    }
    else if(!inner_image.value && !update_inner_image.length>0){
        showValidationError(inner_image,"Inner image is required");
    }
    else if(!client_overview.value){
        showValidationError(client_overview,"Client overview is required");
    }
    else if(!client_says.value){
        showValidationError(client_says,"Client says is required");
    }
    else if(!challenge_description.value){
        showValidationError(challenge_description,"Challenge description is required");
    }
    else if(!solution_description.value){
        showValidationError(solution_description,"Solution description is required");
    }
    else if(!result_description.value){
        showValidationError(result_description,"Result description is required");
    }
    else if(!industries.value){
        showValidationError(industries,"Industries are required");
    }
    else if(!country.value){
        showValidationError(country,"Country is required");
    }
    else{
        return true;
    }
    
}