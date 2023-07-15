// (async function() {
// })();

window.onload = function(e){
    console.log("JS for pinboard manager is ready");

    const btnLabel = 'menu-button';
    const btn = document.getElementById(btnLabel);
    const btnList = document.querySelector('[aria-labelledby=menu-button]');
    btnList.setAttribute('style', 'display:none;');
    // const btnState = btn.getAttribute('aria-expanded');

    btn.setAttribute('aria-expanded', 'false');
    // dropdown_control(btn, btnLabel);

    btn.addEventListener('click', manageDropdown);
}
function dropdown_control(btn, btnLabel){
    const btnList = document.querySelector('[aria-labelledby='+btnLabel+']');
    btn.addEventListener('click',function(e){
        if(btnState == 'true'){
            // btnList.setAttribute('style', 'display:none;');
            btn.setAttribute('aria-expanded', 'false');
        } else if (btnState == 'false'){
            // btnList.setAttribute('style', 'display:block;');
            btn.setAttribute('aria-expanded', 'true');
        }
    });
}
function manageDropdown(e){
    const btn = document.getElementById('menu-button');
    const btnList = document.querySelector('[aria-labelledby=menu-button]');
    const btnState = btn.getAttribute('aria-expanded');

    if(btnState == 'true'){
        btnList.setAttribute('style', 'display:none;');
        btn.setAttribute('aria-expanded', 'false');
    } else if (btnState == 'false'){
        btnList.setAttribute('style', 'display:block;');
        btn.setAttribute('aria-expanded', 'true');
    }
}

// aria-labelledby="menu-button"
