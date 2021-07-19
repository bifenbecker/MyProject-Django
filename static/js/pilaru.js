
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function api_add_item_to_order(btn, item_id) {
    let $btn = $(btn)
    let $span = $btn.find('span');

    let qty = parseInt($btn.parent().parent().find('input[name="item_qty"]')[0].value);

    $.ajax({
        url: '/orders/api/add_item_to_order',
        type: 'post',
        data: { 'item_id': item_id, 'quantity': qty },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) {
            if (data['result'] !== 'ok'){
                alert(data['result'])
            }else{
                let current_qty = parseInt($span.attr('data-count'));
                if (isNaN(current_qty)) {
                    current_qty = 0;
                }
                $span.attr('data-count', current_qty + qty);
            }

        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_remove_item_from_order(item_to_order_id) {
    $.ajax({
        url: '/orders/api/remove_item_from_order',
        type: 'post',
        data: { 'item_to_order_id': item_to_order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) {
            document.location.reload();
        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_change_item_qty_in_order(input, item_to_order_id) {
    let quantity = input.value;
    $.ajax({
        url: '/orders/api/change_item_qty_in_order',
        type: 'post',
        data: { 'item_to_order_id': item_to_order_id, 'quantity': quantity },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });
}


function api_close_order(order_id) {
    $.ajax({
        url: '/orders/api/close_order',
        type: 'post',
        data: { 'order_id': order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e.toString());
        }
    });

}

function SelectOrder(project_name, order_id){
    console.log(project_name)
    $.ajax({
        url: '/orders/api/set_active_order',
        type: 'post',
        data: { 'project_name': project_name, 'order_id': order_id },
        headers: {
            'X-CSRFToken': csrftoken,
        },
        dataType: 'json',
        success: function (data) { 
            var orders_a = Array.prototype.slice.call(document.getElementById('ActiveOrders').querySelectorAll('a'));
            var active_order = orders_a.filter(filterElements)[0];
            active_order.getElementsByClassName('badge badge-pill badge-success')[0].innerHTML = 'Не выбран';
            active_order.getElementsByClassName('badge badge-pill badge-success')[0].className = 'badge badge-pill badge-secondary';
            
        },
        error: function (e) {
            alert('Ошибка запроса к серверу: ' + e['error']);
        }
    });
}

$(document).on('click', function(e) {
    var target = e.target;
    if(target.className === 'dropdown-item d-flex align-items-center' && target.onclick != null){
        var div_status = target.getElementsByClassName('badge badge-pill badge-secondary');
          
        if(div_status.length != 0){
            console.log(div_status[0].innerHTML);  
            div_status[0].innerHTML = 'Активный';
            div_status[0].className = 'badge badge-pill badge-success';
        }
    }
});

function filterElements(element){
    return element.getElementsByClassName('badge badge-pill badge-success').length != 0;
}