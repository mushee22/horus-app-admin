function appVersionValidation(){
    if(!version_name.value){
        showValidationError(version_name,"Version name is required")
    }
    else if(!price.value){
        showValidationError(price,"Price is required")
    }
    else if(!features.value){
        showValidationError(features,"Features are required")
    }
    else if(!modules.value){
        showValidationError(modules,"Modules are is required")
    }
    else if(!description.value){
        showValidationError(description,"Description is required")
    }
    else if(!description2.value){
        showValidationError(description2,"Sub description is required")
    }
    else{
        return true;
    }
}