var div = document.querySelector('.wrap'),
    btn = document.querySelector('.btn1'),
    data = document.querySelector('#inp')


btn.addEventListener('click', () => {
    let p = document.createElement('p')
    let text = document.createTextNode(data.value)
    p.appendChild(text)
    div.appendChild(p)
    div.style.textAlign = 'center'
    div.style.padding = '20px 0'
    data.value = ''

    if(p === 2){
        alert('bunday kiritilmaydi')
        data.value = ''
    }

})