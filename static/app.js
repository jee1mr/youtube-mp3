(function () {

	let searchForm = document.getElementById('search-form');
	searchForm.addEventListener('submit', search);

	function search(e) {
		console.log("Searching..");
		e.preventDefault();
		var keyword = document.getElementById('keyword').value;	
		fetch('/search?q=' + keyword)
		.then(
			function(response){
				return response.json();
			})
		.then(
			function(jsonResponse){
				console.log("Found " + jsonResponse.length + " videos");
				renderResult(jsonResponse);
			})
		.catch(
			function(error){
				console.error(error);
		});
	}

	function makeVideoDiv(video) {
		let divEl = document.createElement('div');
		divEl.setAttribute('class','video-element');
		let titleEl = document.createElement('p')
		titleEl.innerHTML = video.title;
		let imgEl = document.createElement('img');
		imgEl.setAttribute('src',video.thumbnail);
		let buttonEl = document.createElement('button');
		buttonEl.innerHTML = "Convert to mp3";
		buttonEl.setAttribute('data-video-id', video.videoId);
		buttonEl.addEventListener('click', convert);

		divEl.appendChild(imgEl);
		divEl.appendChild(titleEl);
		divEl.appendChild(buttonEl);

		return divEl;
	}

	function renderResult(result) {
		var resultContainer = document.getElementById('result-container');
		resultContainer.innerHTML = '';
		var resultVideos = result.map(function(video){
			resultContainer.appendChild(makeVideoDiv(video));
		});

	}

	function convert(e){
		let that = this;
		var el = e.currentTarget;
		let videoId = el.dataset.videoId;
		console.log("Converting..", videoId);
		fetch('/convert/' + videoId)
		.then(function(response){
			return response.json();
		})
		.then(function(jsonResponse){
			console.log("download link: ", jsonResponse, that);
			makeDownloadMp3Link(that, jsonResponse.downloadUrl);
		})
		.catch(function(error){
			console.error(error);
		});
	}

	function makeDownloadMp3Link(parentDiv, downloadUrl){
		let downloadMp3Link = document.createElement('a');
		downloadMp3Link.innerHTML = 'Download mp3';
		downloadMp3Link.setAttribute('href', downloadUrl);
		downloadMp3Link.setAttribute('target', '_blank');
		parentDiv.innerHTML = "";
		parentDiv.style.backgroundColor = "#1eade6";
		parentDiv.appendChild(downloadMp3Link);
	}

})();