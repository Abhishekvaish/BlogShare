function sendRequest(url,method,data){
	var result = axios({
		url : url,
		method : method ,
		data : data,
		xsrfCookieName : 'csrftoken',
		xsrfHeaderName : 'X-CSRFToken',
		headers : {
			'x-Requested-With':'XMLHttpRequest'
		}
	})
	return result
}

function tranform_chip(e) {
	a = document.querySelector(".chips")
	chips =  M.Chips.getInstance(a).chipsData ;
	tags = ""
	chips.forEach(function(chip){
		if(chip.tag) tags+=(chip.tag+",")
	})
	if (tags){
		document.getElementById("id_tags").value=tags.substring(0,tags.length-1)
		return true
	}
	else{
		document.getElementById("notags").innerText = "Please enter some tags !";
		return false
	}
}
var i = null
function getIndex(j){
	if (j) i = j;
	else {
		if (i){
			let formData = new FormData();
			formData.append('pk',i);
			sendRequest("","POST",formData)
		}
	}
}


var detail_app = new Vue({
	delimiters: ['[[', ']]'],
	el:"#detail",
	data : {
		comments : [],
		comment : "",
		liked : false,
		like_count:0,
		delete_comment_index:null,
	},
	created(){
		host = `${window.location.protocol}//${window.location.host}/`
		if (/\d\/.+/.test(document.URL.replace(host,""))){
			sendRequest("","GET").then((res)=>{
				this.like_count = res.data.like_count
				this.liked = res.data.liked
				this.comments = res.data.comments.sort(function(a,b){
					a = new Date(a.time)
					b = new Date(b.time)
					if (a<b) return 1
					else if(a==b) return 0 
					else return  -1
				})
			})
		}
		
	},
	methods : {
		toggle_like(e){
			if (this.liked){
				this.liked = false
				this.like_count -= 1
				sendRequest(`${document.URL}?like=false`,"GET")
			}else{
				this.liked = true
				this.like_count += 1
				sendRequest(`${document.URL}?like=true`,"GET")
			}
		},
		addComment(e){
			if (this.comment.trim().length != 0 ){
				let formData = new FormData();
				formData.append("text",this.comment) 
				this.comment = ""
				sendRequest(`${document.URL}?comment=true`,"POST",formData)
				.then((res)=>{
					this.comments = res.data.comments.sort(function(a,b){
						a = new Date(a.time)
						b = new Date(b.time)
						if (a<b) return 1
						else if(a==b) return 0 
						else return  -1
					})
				})
				
			}
		},
		delete_comment(){
			if (this.delete_comment_index){
				let formData = new FormData();
				formData.append("pk",this.delete_comment_index)
				sendRequest(`${document.URL}?delete_comment=true`,"POST",formData)
				.then(res => {
					this.comments = res.data.comments.sort(function(a,b){
						a = new Date(a.time)
						b = new Date(b.time)
						if (a<b) return 1
						else if(a==b) return 0 
						else return  -1
					})	
				})
			}
		}
	},

})