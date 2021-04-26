var table = document.getElementsByClassName('table-tasks')[0];
var cont = document.getElementsByClassName('container')[0];

table.addEventListener('wheel', ev => {
    // console.log(ev.deltaX, ev.deltaY);
    if (Math.abs(ev.deltaX) > 0) {
        return;
    }
    if (Math.abs(ev.deltaX) === 0 && Math.abs(ev.deltaY) === 0) {
        return
    }
    // console.log('scrolling')
    var scrollX = 77;
    if (ev.deltaY < 0) {
        scrollX *= -1;
    }
    table.scrollBy({
        top: 0,
        left: scrollX,
        // behavior: 'smooth'
    });
});

window.addEventListener('resize', ev => {
    if (table.scrollWidth > table.clientWidth) {
        cont.classList.add('scrollbar');
    } else {
        cont.classList.remove('scrollbar');
    }
})

if (table.scrollWidth > table.clientWidth) {
        cont.classList.add('scrollbar');
}