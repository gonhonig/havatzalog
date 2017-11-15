var notify_badge_id;
var notify_menu_id;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

function fill_notification_badge(data) {
    var badge = document.getElementById(notify_badge_id);
    if (badge) {
        badge.innerHTML = data.unread_count;
    }
}

function fill_notification_list(data) {
    var menu = document.getElementById(notify_menu_id);
    if (menu) {
        var count = data.unread_list.length;
        if (count == 0){
            document.getElementById('notif-icon').className = 'nav-link oi oi-globe pr-1';
        } else {
            document.getElementById('notif-icon').className = 'nav-link oi oi-globe pr-1 text-danger';
        }
        var content = [];
        menu.innerHTML = data.unread_list.map(function (item) {
            var message = "";
            var url = "#";
            if(typeof item.verb !== 'undefined'){
                message = item.verb;
            }
            if(typeof item.description !== 'undefined'){
                url = item.description;
            }
            return '<a class="dropdown-item" href="'+ url +'">' + message + '</a>';
        }).join('')
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function(event){
            if (this.readyState === 4){
                if (this.status === 200){
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    registered_functions.forEach(function (func) { func(data); });
                }else{
                    consecutive_misfires++;
                }
            }
        });
        // r.open("GET", notify_api_url+'?max='+notify_fetch_count, true);
        r.open("GET", notify_api_url+'?max='+notify_fetch_count+'&mark_as_read=true', true);
        r.send();
    }
    if (consecutive_misfires >= 10) {
        var badge = document.getElementById(notify_badge_id);
        if (badge) {
            badge.innerHTML = "!";
            badge.title = "Connection lost!"
        }
    }
}

setTimeout(fetch_api_data, 0)
