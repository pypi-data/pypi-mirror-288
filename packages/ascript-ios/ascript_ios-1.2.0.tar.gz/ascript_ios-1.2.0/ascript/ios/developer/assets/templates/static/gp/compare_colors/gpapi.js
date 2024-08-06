var api;
var colors = new Array(9)
var gp;

var p_max_nums = 1

var task = {
    params:"",
    data:{}
}

function on_load(p_gp,gp_api) {
    gp = p_gp
    $("#title").text(gp.name)
    // alert(gp)
    api = gp_api;

    for (let i = 0; i < colors.length; i++) {
        var color_dom = $("#color_item").clone()
        color_dom.attr("id", undefined)
        color_dom.addClass("color_item")
        color_dom.appendTo("#colors_list")
        color_dom.find(".color_item_number").text(i + 1)
        var color_xy = color_dom.find(".color_item_xy_color");
        color_xy.attr("placeholder", `键盘快捷按键 ${i + 1}`)
    }

    $("#find_color_diff").blur(function(){
        make_data()
    })

    $("#find_colors_submit").click(function(){
        make_data();
        api.strack.add(task)
    })

    $("#btn_reset_all_colors").click(function () {
        $(".color_item_xy_color").val("")
        $(".color_item_color").css("background-color", "whitesmoke")
        make_data()
    })

    $("#find_colors_test").click(function(){
        make_data();
        $("#find_colors_test_loading").show()
        api.strack.test(task,on_data)
    })

    $("#findcolor_code").dblclick(function () {
        var val = $("#findcolor_code").val();
        copy(val)
        api.sys.alert("复制:" + val)
    })

    $.contextMenu({
        selector: "#findcolor_code",
        trigger: 'right',
        // define the elements of the menu
        items: {
            copy_params: {
                name: "复制参数", callback: function (key, opt) {
                    copy(task.params)
                    api.sys.alert("复制:"+task.params)
                    // , opt.$trigger.text()
                    //   alert(opt.$trigger.attr("i"))
                    // opt.$trigger.remove()
    
                }
            },
            copy_all: {
                name: "复制全部", callback: function (key, opt) {
                    var val = $("#findcolor_code").val();
                    copy(val)
                    api.sys.alert("复制:"+val)
                    // , opt.$trigger.text()
                    //   alert(opt.$trigger.attr("i"))
                    // opt.$trigger.remove()
    
                }
            },
        }
        // there's more, have a look at the demos and docs...
    });
}

function on_roload(p_gp) {
    
    gp = p_gp

    if (gp.data) {

    } else {
        // alert("n nid")
    }
}

function on_rect(rect) {
}

function on_data(data) {
    $("#find_colors_test_loading").hide()
    if(data.data){
        alert("颜色比对成功")
    }else{
        alert("颜色比对失败")
    }
}

// 当按键按下后,会通知
function on_color(key, color) {
    // alert(key)
    var key_index = Number(key) - 1

    color[key_index] = color
    //  alert(key_number)
    var dom = $("#colors_list").children().eq(key_index);
    var color_input = dom.find(".color_item_xy_color");
    color_input.val(`${color.x},${color.y + ",#" + color.c}`);
    var color_disc = dom.find(".color_item_color");
    color_disc.css("background-color", "#" + color.c)

    var color_del = dom.find(".color_item_del");
    color_del.click(function () {
        $(color_input).val("")
        color_disc.css("background-color", "whitesmoke")
    })

    make_data()

}

// -- 自定义

function test_data() {
    

}

function make_data() {
    colors_array = $(".color_item_xy_color").map(function () {
        return $(this).val().trim(); // 获取并去除字符串两端的空格  
    }).get().filter(function (value) {
        return value !== ''; // 过滤掉空字符串  
    });

    task.data["colors"] = `"${colors_array.join('|')}"`

    task.params = task.data["colors"]

    var diff_str = $("#find_color_diff").val().trim();
    if (diff_str.length > 0 && diff_str != "0.9") {
        var diff = `,diff=${diff_str}`;
        task.params = task.params + diff
        task.data["diff"] = diff_str
        // data.push(diff);
    }else{
        task.data["diff"] = null
    }

    mk_code()

}

function get_rect() {
    var rect = []
    for (let i = 0; i < input_list.length; i++) {
        var num_str = input_list[i].val()
        if (num_str.length > 0) {
            rect[i] = Number(num_str)
        } else {
            return rect
        }
    }
    return rect
}

function mk_code(){

    var fcode = `CompareColors(${task.params}).compare()`

    $("#findcolor_code").val(fcode)
}

function copy(msg){
    // alert(msg)
    var createInput = document.createElement("input");
    createInput.value = msg;
    document.getElementById("res_no").appendChild(createInput);
    createInput.select();
    document.execCommand("Copy");
    createInput.className = 'createInput';
    createInput.style.display = "none";

    // alert(createInput.value)
}

function copy(msg){
    // alert(msg)
    var createInput = document.createElement("input");
    createInput.value = msg;
    document.getElementById("find_color_con").appendChild(createInput);
    createInput.select();
    document.execCommand("Copy");
    createInput.className = 'createInput';
    createInput.style.display = "none";

    // alert(createInput.value)
}