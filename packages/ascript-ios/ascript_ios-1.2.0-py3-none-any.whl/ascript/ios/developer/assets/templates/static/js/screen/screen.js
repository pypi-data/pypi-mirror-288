
var image = document.getElementById('img_preview');
var img_deleft_dom;
var conimg = $("#container_img");
var image_data_object;
const uploadDir = "/sdcard/airscript/screen/upload/"

var mouse_move_xyc = {};
var is_mouse_downed = false;
var is_show_box = false;
var part_box = $("#part_box");

var source_path = null;

var gp_path = null

var gpobj = undefined;

var image_list_res = undefined;

var image_list_max_show = 5

var is_imgcon_mouse_down = false
var is_iframecon_mouse_down = false

var device_id = getQueryString('device_id')

$(document).ready(function () {
    gpapi.strack.load()
    // clearGpImage()
    getImgList(true)
    initImgLogic()
    initImageListLogic()
    $('[data-toggle="tooltip"]').tooltip()
    init_Image_Mouse()
    init_key_logic()
    init_as_moduls()
    getGpLineList()
    dragChangeContainer()
    
    // initIframe()
    // gpiframeout()

    // api_marks_point_add(1,[100,200])
    // api_marks_point_add(2,[300,400])
});

// function gpiframeout(){
//     var iframe = document.querySelector('iframe');  
//     iframe.onload = function() {  
//         if (iframe.contentWindow && iframe.contentWindow.document) {  
//             // 注意：这仅在同源时有效  
//             iframe.contentWindow.document.addEventListener('keydown', function(event) {  
//                 console.log('Keydown event inside iframe (if same-origin):', event.key);  
//             });  
//         }  
//     };  
// }

function dragChangeContainer(){
    var src_posi_Y = 0, src_posi_X = 0, dest_posi_Y = 0, dest_posi_X = 0, move_Y = 0, destHeight = 0, destWidth = 0, moveed = false, right = 0, bottom = 0, consleHeight,height =0;

    $(".touch_slide")
      .mousedown(function (e) {
        is_imgcon_mouse_down = true;
        src_posi_Y = e.pageY;
        src_posi_X = e.pageX;
        // alert(right);
        right = $(".screen-img-container").width()
        // e.stopPropagation()
    });

    $(".gp_touch_bar")
      .mousedown(function (e) {
        is_iframecon_mouse_down = true;
        src_posi_Y = e.pageY;
        src_posi_X = e.pageX;
        // alert(right);
        height = $(".coder-iframe").height()
        // e.stopPropagation()
    });

    $(document).bind("click mouseup", function (e) {
      if (is_imgcon_mouse_down) {
        is_imgcon_mouse_down = false;
        moveed = false;
      }

      if (is_iframecon_mouse_down) {
        is_iframecon_mouse_down = false;
        moveed = false;
      }
    })
      .mousemove(function (e) {

        if (is_imgcon_mouse_down) {
          
          dest_posi_Y = e.pageY;
          dest_posi_X = e.pageX;
          move_X = dest_posi_X - src_posi_X;
          move_Y = dest_posi_Y - src_posi_Y;

          // alert(right + move_X)
          if (right + move_X > 20) {
            // console.log(right + move_X + "px")
            $(".screen-img-container").width(right + move_X + "px");
          }

          moveed = true;

          e.preventDefault();
        }

        if (is_iframecon_mouse_down) {
          
            dest_posi_Y = e.pageY;
            dest_posi_X = e.pageX;
            move_X = dest_posi_X - src_posi_X;
            move_Y = dest_posi_Y - src_posi_Y;
  
            // alert(right + move_X)
            if (height + move_Y > 20) {
              // console.log(right + move_X + "px")
              $(".coder-iframe").height(height + move_Y + "px");
            }
  
            moveed = true;
  
            e.preventDefault();
          }


      });
}

function clearGpImage() {
    $.ajax({
        url: `${baseUrl}/api/gp/image/clear`,
        type: 'get',
        data: {},
        async: true,
        success: function (res) {
            // alert(res.data.length)
            // imglist = res.data;
        },
        error: function (err) {
            $("#imagelist_loading").hide();
            alert(err)
        }
    })
}

function initImgLogic() {
    image = document.getElementById('img_preview');
    $("#img_preview").on('load', function () {
        // $("#image_loading").hide();
        $("#imagelist_loading").hide();
        image_data_object = getImageData();
        // $(conimg).scrollLeft(0)
        // $(conimg).scrollTop(0)

        $('#header_pixels').text(`${image.width}x${image.height}`)
        $(".zoomWindow").css("background-size", `${image.width}px ${image.height}px`)
        // alert($(image).height()+"?"+image.width

        if (image.height > image.width) {
            $(image).css("height", "100%");
            $(image).css("width", "auto");
        } else {
            $(image).css("width", "100%");
            $(image).css("height", "auto");
        }

        changeImageMarkSize()
    })

    $("#toolbar_img_delall").click(function (e) {
        $("#toolbar_img_delall_loading").show()

        var path_dir = $(image).attr('path')
        path_dir = path_dir.substring(0, path_dir.lastIndexOf('/'))
        // alert(path_dir)

        $.ajax({
            url: `${baseUrl}/api/file/remove`,
            type: 'post',
            data: { path: path_dir },
            async: true,
            success: function (res) {
                $(".screen-img-list").empty();
                $(".imglist_size").text(0);
                $("#toolbar_img_delall_loading").fadeOut(500)
            },
            error: function (err) {
                alert('删除异常')
            }
        })
    });

    $("#delect_img").click(function (e) {
        // alert(1)
        img_deleft_dom.remove();
        $("#delect_img").hide();

        $.ajax({
            url: `${baseUrl}/api/file/remove`,
            type: 'post',
            data: { path: $(img_deleft_dom).attr('i') },
            async: false,
            success: function (res) {
                $(".imglist_size").text($(".screen-img-list").children().length);
                // mk_image_show_no()
                // alert('12')
            },
            error: function (err) {
                alert('删除异常'+JSON.stringify(err))
            }
        })

        // $(img_deleft_dom).animate({ width: 0 }, 400);
    });

    $("#toolbar_img_capture").click(function (e) {
        getImgList(true);
    });

    $("#toolbar_img_upload").click(function (e) {
        // alert('1')
        uploadFile(uploadDir);
    });

    $("#toolbar_zoom_in").click(function (e) {

        var rect = gpapi.image.get_rect()

        if(rect.length>3){
            var width = (rect[2] -rect[0]) * 0.1
            var height = (rect[3]-rect[1]) * 0.1
            var n_rect = [rect[0]+width,rect[1]+height,rect[2]-width,rect[3]-height]
            gpapi.image.set_rect(n_rect)
        }else{
            $(image).css("height", image.height * 1.1);
            $(image).css("width", "auto");
            changeImageMarkSize();
        }
        
        e.stopPropagation(); //阻止传递事件
    });

    $("#toolbar_zoom_out").click(function (e) {

        var rect = gpapi.image.get_rect()

        if(rect.length>3){
            var width = (rect[2] -rect[0]) * 0.1
            var height = (rect[3]-rect[1]) * 0.1
            var n_rect = [rect[0]-width,rect[1]-height,rect[2]+width,rect[3]+height]
            gpapi.image.set_rect(n_rect)

        }else{
            //无范围时,
            $(image).css("height", image.height * 0.9);
            $(image).css("width", "auto");
            changeImageMarkSize();
        }

        
        e.stopPropagation(); //阻止传递事件
    });

    $("#toolbar_zoom_reset").click(function (e) {

        // scope_pos = [null, null];


        if (image.height > image.width) {
            $(image).css("height", "100%");
            $(image).css("width", "auto");
        } else {
            $(image).css("width", "100%");
            $(image).css("height", "auto");
        }

        $(conimg).scrollLeft(0)
        $(conimg).scrollTop(0)

        changeImageMarkSize()

        // part_box.css("left", "0px");
        // part_box.css("top", "0px");
        // part_box.css("width", "0px");
        // part_box.css("height", "0px");
        // part_box.css("display", "none");

        // changeImageMarkSize();

    });

    // $("#coder-board-header-reset").click(function () {
    //     $("#imagelist_loading").show();
    //     // excute_gpjob(-1)
    //     gpapi.strack.run(on_strack_run_result, -1)
    //     $(".coder-board-body-item").removeClass('coder-board-body-item-active');
    // })

    $("#coder-board-reset").click(function () {
        // alert("1")
        gpapi.strack.clear()
        $("#imagelist_loading").show();
        gp_path = source_path
        showImg(source_path)
    })

    $("#coder-board-result").click(function () {
        // alert("123")
        if (gpapi.strack.result) {
            alert(JSON.stringify(gpapi.strack.result, null, 2))
        } else {
            alert("没有结果,是否有任务处理?")
        }
    })

    $("#toolbar_mask_clear").click(function () {
        gpapi.marks.point.clear()
        gpapi.marks.rect.clear()

    })

    $("#btn_strack_reset").click(function () {
        gpapi.strack.clear()
        gpapi.marks.point.clear()
        gpapi.marks.rect.clear()
    })

    $("#gp_export_name").on("input", function (e) {
        var name = $("#gp_export_name").val().trim()
        api_strack_genor_code(name)
    })

    $("#btn_strack_export").click(function () {
        // gpapi.strack.export()
        $("#gp_export_name").val(gpapi.strack.info.gpname)
        api_strack_genor_code(gpapi.strack.info.gpname)
        $('#gp_export').modal('show')

        var init_file_path = gpapi.strack.info.path + "/__init__.py"
        gpapi.file.read(init_file_path, function (res) {
            $("#gp_module_code").val(res)
        })
    })

    $("#gp_export_submitf").click(function () {

        var activeTab_id = $('.nav-item .active').attr("id");

        if (activeTab_id === "e_pg") {
            // 保存为GP文件
            var path = gpapi.module.current.path;
            var name = $("#gp_export_name").val().trim()
            $("#gp_export").modal("hide")
            // api_sys_copy_modal($("#gp_export_code").val())
            api_sys_copy_form($("#gp_export_code").val(), "gp_export_code")
            gpapi.strack.export(path, name)
        } else {
            //将GP数据全部复制进工程
            var path = gpapi.module.current.path+"/res";
            var s_path = gpapi.strack.info.path+"/res"
            api_sys_copy_form($("#gp_module_code").val(), "gp_module_code")
            $("#gp_export_submitf_loading").show()
            gpapi.file.copy(s_path,path,function(e){
                $("#gp_export_submitf_loading").hide()
                $("#gp_export").modal("hide")
            })

        }


    })

    $("#as_alert_close").click(function () {
        $("#as_alert").hide()
    })

    $("#header_color_current").focus(function () {
        api_sys_copy_form($(this).val(), "header_color_current")
    })

    $("#image_input_rect").focus(function () {
        api_sys_copy_form($(this).val(), "image_input_rect")
    })

    $("#image_input_rect").blur(function () {
        var rect_str = $(this).val().trim()
        if(rect_str.length>0){
            let rect = rect_str.split(',').map(Number);
            if(rect.length==4){
                gpapi.image.set_rect(rect,true)
            }
        }
    })

    $("#gp_test").click(function () {
        $("#gp_test_modal").modal("show")
    })

    $("#gp_test_submit").click(function () {
        var m_name = $("#gp_test_name").val()
        if (m_name.length < 1) {
            alert("请填写文件名")
            return
        }

        $.ajax({
            url: `${baseUrl}/api/gp/test`,
            type: 'post',
            data: { name: m_name },
            async: true,
            success: function (res) {
                if (res.code == 1) {
                    // alert("成功")
                    get_gpplug_list()
                    $("#gp_test_modal").modal("hide")
                } else {
                    alert(res.msg)
                }
            },
            error: function (err) {
                alert(err)
            }
        })
    })

    $("#gp_plugs").click(function () {
        $("#gp_line_modal").modal("show")
    })

    $("#toolbar_eraser_wipe").click(function () {

        // alert("??")

        var path = gp_path;
        var rect = JSON.stringify(api_get_rect())


        $.ajax({
            url: `${baseUrl}/api/gp/img/wipe`,
            type: 'post',
            data: { path: path, rect: rect },
            async: true,
            success: function (res) {
                // alert(res.data.length)
                if (res.code == 1) {
                    showImg(path)
                    if (gpframe && gpframe.contentWindow && gpframe.contentWindow.on_wipe) {
                        gpframe.contentWindow.on_wipe()
                    }
                }
            },
            error: function (err) {
                $("#imagelist_loading").hide();
                alert(err)
            }
        })
    });

    $("#header_key_focus").click(function(){
        gpapi.sys.alert("可以取色啦~")
    })

}

function getImgList(cap) {
    $(".screen-img-list").empty();
    $("#imagelist_loading").show();
    $.ajax({
        url: `${baseUrl}/api/screen/capture/list?device_id=${device_id}&capture=${cap}`,
        type: 'get',
        data: {},
        async: true,
        success: function (res) {
            // alert(res.data.length)
            // imglist = res.data;
            image_list_res = res;

            // alert(JSON.stringify(res,0,2))

            if (res.data.length > 0) {
                var item = res.data[0]
                //获取列表后,给
                // showImg(item.path)
                source_path = item.path;
                // // excute_gpjob()
                gpapi.strack.run(on_strack_run_result);
            }

            fill_imagelist_items(res)

            $(".imglist_size").text(res.data.length);
            // mk_image_show_no()

            // $(".screen-img-list-con").hide();


        },
        error: function (err) {
            $("#imagelist_loading").hide();
            alert(err)
        }
    })
}

function mk_image_show_no() {
    var curren_no = image_list_max_show;
    var max_no = image_list_res.data.length;
    $("#screen-imglist-bar-no").text(`${curren_no}/${max_no}`)
}



function fill_imagelist_items(res) {
    if (res.data.length > 0) {

        // if(image_list_max_show>image_list_res.data.length){
        //     image_list_max_show = image_list_res.data.length
        // } 

        var all_add = $(".screen-img-list").children().length;
        for (let i = all_add; i < res.data.length; i++) {
            item = res.data[i]

            var dom = $("#image_list_item").clone();
            dom.attr("id", "")
            dom.attr("i", item.path)
            var p_src = `${baseUrl}/api/file/get/image?path=${item.path}&maxheight=${100}`
            if (i < image_list_max_show) {
                dom.attr("src", p_src)
                dom.attr("srch", "")
            } else {
                dom.attr("src", "")
                dom.attr("srch", p_src)
            }

            dom.attr("title", `${item.name}\n${item.lastModified_format}\n${item.length_format}`)
            dom.appendTo(".screen-img-list");
        }

        // mk_image_show_no()


        // alert(all_add)
        // res.data.forEach((item, index, arr) => {
        //     if (index + 1 < all_add) {
        //         if (index >= image_list_max_show) {
        //             return
        //         }

        //         var dom = $("#image_list_item").clone();
        //         var p_src = `${baseUrl}/api/file/getpicture?path=${item.path}&maxheight=${100}`
        //         dom.attr("i", item.path)
        //         dom.attr("src", p_src)
        //         dom.attr("title", `${item.name}\n${item.lastModified_format}\n${item.length_format}`)
        //         dom.appendTo(".screen-img-list");
        //     }
        //     // $(`<img  i="${item.path}"  class="screen-img-list-item ml-2" title="${item.name}\n${item.lastModified_format}\n${item.length_format}" src="${baseUrl}/api/file/getpicture?path=${item.path}&maxheight=${$(".screen-img-list").height()}">`).appendTo(".screen-img-list");
        // });
        $(".screen-img-list-item").eq(0).addClass("shoadow-lg-green");
        $(".screen-img-list-item").eq(0).addClass("screen-img-list-item-active");
    }

    $(".screen-img-list-item").mousemove(imagelist_mouseover);
    $(".screen-img-list-item").click(function (e) {
        // clearmarks();
        // scope_pos = [null, null];
        // showImg($(e.target).attr('i'))
        source_path = $(e.target).attr('i');
        // excute_gpjob()
        // gpapi.strack.run(on_strack_run_result);
        // $("#image_loading").show();
        // image.src = `${baseUrl}/api/file/get/image?path=${$(e.target).attr('i')}`
        showImg($(e.target).attr('i'))
        // $(image).attr('path', $(e.target).attr('i'));
        // $(".zoomWindow").css("background-image", `url('${image.src}')`)
        $(".screen-img-list-item").removeClass("shoadow-lg-green");
        $(".screen-img-list-item").removeClass("screen-img-list-item-active");
        $(e.target).addClass("shoadow-lg-green");
        $(e.target).addClass("screen-img-list-item-active");

        // $(".screen-img-list-con").hide();

    });
}

function imagelist_mouseover(e) {

    var srch = $(this).attr("srch")
    if (srch.length > 0) {
        $(this).attr("src", srch)
        $(this).attr("srch", "");
    }


    $("#delect_img").show();
    // alert("")

    // alert($(e.target).attr('src'))
    var dom = $(e.target);
    img_deleft_dom = $(e.target);
    var left = dom.width() + dom.position().left - dom.scrollLeft() - $("#delect_img").width() + 13;
    // alert(left)
    $("#delect_img").css("left", left + "px");
}

function showImg(url) {

    $("#part_box").removeClass("shadow-lg");
    part_box.css("left", "0px");
    part_box.css("top", "0px");
    part_box.css("width", "0px");
    part_box.css("height", "0px");
    part_box.css("display", "none");

    $("#image_loading").show();
    image.src = "";
    image.src = `${baseUrl}/api/file/get/image?path=${url}&t=${Date.now()}`;
    // alert(image.src)
    $(image).attr("path", url);





    // $(image).attr("src", `${baseUrl}/api/file/getpicture?path=${url}`);
    // alert("123")
    $(".zoomWindow").css("background-image", `url('${image.src}')`)
}

function getImageData() {
    $(image).css("height", "auto");
    $(image).css("width", "auto");
    var cvs = document.getElementById('preview_img_canvas');
    cvs.width = image.width;
    cvs.height = image.height;
    var ctx = cvs.getContext('2d');
    var dimImage = document.getElementById('img_preview')
    ctx.drawImage(dimImage, 0, 0);
    return ctx.getImageData(0, 0, dimImage.width, dimImage.height);
}

var image_list_filled = false
function initImageListLogic() {
    $("#imglist_size").mouseover(function () {
        // alert($(".screen-img-list-con").is(':visible'))
        if (!$(".screen-img-list-con").is(':visible')) {
            $(".screen-img-list-con").fadeIn(100);
        }

        // alert($(".screen-img-list").children().length)
        // if(!image_list_filled){
        //     image_list_filled = true
        //     fill_imagelist_items(image_list_res);
        // }
    })

    $(".screen-img-list-con").mouseleave(function () {
        $(".screen-img-list-con").hide();
    })
}

function uploadFile(p) {
    $("#fileupload").trigger('click');
    $("#fileupload").change(function (e) {
        // alert($('#fileupload')[0].files.length)
        $("#imagelist_loading").show();
        if ($('#fileupload')[0].files.length >= 1) {
            var formData = new FormData();
            var fName = $('#fileupload')[0].files[0].name;
            // var fName = new Date().getTime()+".png"
            formData.append("data", e.target.files[0]);
            // formData.append("path", uploadDir+fName);
            $.ajax({
                url: baseUrl + '/api/file/upload?path=' + (uploadDir + fName),
                type: 'POST',
                cache: false,
                data: formData,
                processData: false,
                contentType: false
            }).done(function (res) {
                // $("#upload_pic").text("导入图片");
                // addPicCacheListItem(fName,false)
                getImgList(false)
                $("#imagelist_loading").hide();

            }).fail(function (res) {
                // getFilesList();
                // $("#upload_pic").text("导入图片");
                alert("上传失败")
                $("#imagelist_loading").hide();
            });
        } else {
            // $("#upload_pic").text("导入图片");
            $("#imagelist_loading").hide();
        }

    });
}


function init_key_logic() {
    $(document).keypress(function (e) {
        // alert("22")
        var keynumber = e.keyCode - 48;
        if (keynumber > 0 && keynumber < 10 && is_image_mouseover) {

            gpframe = document.getElementById("gpiframe")

            // alert(JSON.stringify(mouse_move_xyc))
            $("#header_color_current").val(`${mouse_move_xyc.x},${mouse_move_xyc.y},#${mouse_move_xyc.c}`)

            if (gpframe && gpframe.contentWindow.gp) {
                gpframe.contentWindow.on_color(keynumber, mouse_move_xyc)

            }
            // alert("1")
            // on_color

            // var cdom = $("#choose_colors_item_"+keynumber);
            // cdom.find(".choose_colors_item_input").val(mouse_move_xyc.x+","+mouse_move_xyc.y+" #"+mouse_move_xyc.c)
            // cdom.find(".choose_colors_item_bgcolor").css("background-color","#"+mouse_move_xyc.c)
            // chooseColors[keynumber] = mouse_move_xyc;
            // makeFindColorsStr();

            // var bgitemdom = cdom.find(".choose_colors_item_bgcolor")

        }

        // print(cdom.val())
    });

}

function init_as_moduls() {
    gpapi.module.get_all(function (data) {
        $(".as_modules").empty();
        // if(data.data.length<1){
        //     $("#model_create").click();
        //     return;
        // }
        data.data.forEach(function (e, index) {
            if (index == 0) {
                gpapi.module.current = e
                // alert(JSON.stringify(e))
            }
            var item = $(`<option value="${index}">${e.name}</option>`);
            $(".as_modules").append(item);

        });
        gpapi.module.all = data.data;
    })

    $(".as_modules").change(function () {
        // alert($(this).val())
        gpapi.module.current = gpapi.module.all[Number($(this).val())];

        // alert(gpapi.module.current.name)
    })

}

function delect_gptest_module(m_name) {
    // alert(m_name)
    $.ajax({
        url: `${baseUrl}/api/gp/test/remove`,
        type: 'post',
        data: { name: m_name },
        async: true,
        success: function (res) {
            if (res.code == 1) {
                // alert("成功")
            } else {
                alert(res.msg)
            }
        },
        error: function (err) {
            alert(err)
        }
    })
}

function delect_gpline_module(m_name) {
    // alert(m_name)
    $.ajax({
        url: `${baseUrl}/api/gp/plug/remove`,
        type: 'post',
        data: { name: m_name },
        async: true,
        success: function (res) {
            if (res.code == 1) {
                // alert("成功")
            } else {
                alert(res.msg)
            }
        },
        error: function (err) {
            alert(err)
        }
    })
}

function getGpLineList() {
    var url = "http://py.airscript.cn/api/web/plug/list?limit=10000&gp=1";
    $.ajax({
        url: url,
        type: 'get',
        data: {},
        async: true,
        success: function (res) {
            if (res.code == 1) {
                // alert(res)
                fill_GPLineList(res)
            } else {
                alert(res.msg)
            }
        },
        error: function (err) {
            alert(err)
        }
    })
}

function fill_GPLineList(res) {
    res.data.forEach((item, index) => {
        // gp_line_list
        var dom = $("#gp_line_list_item").clone()
        dom.find(".gp_id").text(item.name + ":" + item.version)
        dom.find(".gp_author").text(item.auth);
        dom.find(".gp_hot").text(item.download);
        dom.find(".gp_add").click(function () {
            $(this).addClass("gploading")
            $(this).text("加载中")
            $(this).prop('disabled', true); 
            add_line_gp(item.name + ":" + item.version,function(is_success){
                $(".gploading").prop('disabled', false); 
                if(is_success){
                    $(".gploading").text("已加载")
                }else{
                    $(".gploading").text("重试")
                }
                $(".gploading").removeClass("gploading")
                
            })
            
            // $(this).prop('disabled', true);

        })

        dom.find(".gp_info").click(function () {
            window.open(`http://dev.airscript.cn/plug?id=${item.id}`, "_blank")
        })

        var domcs = dom.find(".gp_line_childs");

        item.gp.forEach((citem, index) => {
            var domc = $("#gp_line_list_item_child").clone()
            domc.find(".gp_line_id").text(citem.id)
            domc.find(".gp_line_des").text(citem.des)
            domc.appendTo(domcs)
        });


        dom.appendTo("#gp_line_list")
    });
}

function add_line_gp(gp_name,listener) {
    $.ajax({
        url: `${baseUrl}/api/gp/plug`,
        type: 'post',
        data: { name: gp_name },
        async: true,
        success: function (res) {
            if (res.code == 1) {
                get_gpplug_list()
                if(listener){
                    listener(true)
                }
                // alert("成功")
                // get_gpplug_list()
                // $("#gp_test_modal").modal("hide")
            } else {
                if(listener){
                    listener(true)
                }
                alert(res.msg)
            }
        },
        error: function (err) {
            alert(err)
        }
    })
}
