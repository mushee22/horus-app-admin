const clickMenu = (e)=>{
    localStorage.setItem('selected',e);
}

window.addEventListener('load',()=>{
    let links = document.querySelectorAll('.nav-link');
    links.forEach(link=>{
        if(link==localStorage.getItem('selected')){
            link.classList.add('active');
            link.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        else{
            link.classList.remove('active');
        }
    })
})