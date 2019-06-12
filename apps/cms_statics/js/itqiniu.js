let itqiniu = {
	'setUp': function(args) {
		let domain = args['domain'];
		let params = {
            browse_button:args['browse_btn'],
			runtimes: 'html5,flash,html4', //上传模式，依次退化
			max_file_size: '500mb', //文件最大允许的尺寸
			dragdrop: false, //是否开启拖拽上传
			chunk_size: '4mb', //分块上传时，每片的大小
			uptoken_url: args['uptoken_url'], //ajax请求token的url
			domain: domain, //图片下载时候的域名
			get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
			auto_start: true, //如果设置了true,只要选择了图片,就会自动上传
            unique_names: false,
            save_key: true,
            multi_selection: false,
            filters: {
                mime_types :[
                    {title:'Image files',extensions: 'jpg,gif,png,jpeg'},
                    {title:'Video files',extensions: 'flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4'}
                ]
            },
			log_level: 5, //log级别
			init: {
				'FileUploaded': function(up,file,info) {
					if(args['success']){
						let success = args['success'];
						let obj = JSON.parse(info);
						let domain = up.getOption('domain');
						file.name = domain + obj.key;
						success(up,file,info);
					}
				},
				'Error': function(up,err,errTip) {
					if(args['error']){
						let error = args['error'];
						error(up,err,errTip);
					}
				},
                'UploadProgress': function (up,file) {
                    if(args['progress']){
                        args['progress'](up,file);
                    }
                },
                'FilesAdded': function (up,files) {
                    if(args['fileadded']){
                        args['fileadded'](up,files);
                    }
                },
                'UploadComplete': function () {
                    if(args['complete']){
                        args['complete']();
                    }
                }
			}
		};

		// 把args中的参数放到params中去
		for(let key in args){
			params[key] = args[key];
		}
		let uploader = Qiniu.uploader(params);
		return uploader;
	}
};
