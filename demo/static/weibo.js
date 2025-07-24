var timeString = function(timestamp) {
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

var commentsTemplate = function(comments) {
    var html = ''
    for(var i = 0; i < comments.length; i++) {
        var c = comments[i]
        var t = `
            <div>
                ${c.content}
            </div>
        `
        html += t
    }
    return html
}

var WeiboTemplate = function(Weibo) {
    var content = Weibo.content
    var id = Weibo.id
    var comments = commentsTemplate(Weibo.comments)
    var t = `
        <div class='weibo-cell' data-id=${id}>
            <div>
                [WEIBO]: ${content}
            </div>
            <div class="comment-list">
                ${comments}
            </div>
            <div class="comment-form">
                <input type="hidden" name="weibo_id" value="">
                <input name="content">
                <br>
                <button class="comment-add">添加评论</button>
            </div>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="Weibo-cell">
        <button class="Weibo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(Weibo)
    */
}

var insertWeibo = function(Weibo) {
    var WeiboCell = WeiboTemplate(Weibo)
    // 插入 Weibo-list
    var WeiboList = e('.weibo-list')
    WeiboList.insertAdjacentHTML('beforeend', WeiboCell)
}

var insertEditForm = function(cell) {
    var form = `
        <div class='Weibo-edit-form'>
            <input class="Weibo-edit-input">
            <button class='Weibo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        // console.log('load all', r)
        // 解析为 数组
        var Weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < Weibos.length; i++) {
            var Weibo = Weibos[i]
            insertWeibo(Weibo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-Weibo')
        var title = input.value
        log('click add', title)
        var form = {
            'title': title,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var Weibo = JSON.parse(r)
            insertWeibo(Weibo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var WeiboList = e('.Weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('Weibo-delete')){
            // 删除这个 Weibo
            var WeiboCell = self.parentElement
            var Weibo_id = WeiboCell.dataset.id
            apiWeiboDelete(Weibo_id, function(r){
                log('删除成功', Weibo_id)
                WeiboCell.remove()
            })
        }
    })
}

var bindEventWeiboEdit = function() {
    var WeiboList = e('.Weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('Weibo-edit')){
            // 删除这个 Weibo
            var WeiboCell = self.parentElement
            insertEditForm(WeiboCell)
        }
    })
}


var bindEventWeiboUpdate = function() {
    var WeiboList = e('.Weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    WeiboList.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('Weibo-update')){
            log('点击了 update ')
            //
            var editForm = self.parentElement
            // querySelector 是 DOM 元素的方法
            // document.querySelector 中的 document 是所有元素的祖先元素
            var input = editForm.querySelector('.Weibo-edit-input')
            var title = input.value
            // 用 closest 方法可以找到最近的直系父节点
            var WeiboCell = self.closest('.Weibo-cell')
            var Weibo_id = WeiboCell.dataset.id
            var form = {
                'id': Weibo_id,
                'title': title,
            }
            apiWeiboUpdate(form, function(r){
                log('更新成功', Weibo_id)
                var Weibo = JSON.parse(r)
                var selector = '#Weibo-' + Weibo.id
                var WeiboCell = e(selector)
                var titleSpan = WeiboCell.querySelector('.Weibo-title')
                titleSpan.innerHTML = Weibo.title
//                WeiboCell.remove()
            })
        }
    })
}

var bindEvents = function() {
//    bindEventWeiboAdd()
//    bindEventWeiboDelete()
//    bindEventWeiboEdit()
//    bindEventWeiboUpdate()
}

var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
