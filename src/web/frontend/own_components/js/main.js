/// <reference path="../../bower_components/DefinitelyTyped/jquery/jquery.d.ts"/>
/// <reference path="../../bower_components/DefinitelyTyped/bootstrap/bootstrap.d.ts"/>
// $('.grid').masonry({
//   itemSelector: '.grid-item', // use a separate class for itemSelector, other than .col-
//   columnWidth: '.grid-sizer',
//   percentPosition: true
// }); 


 

	// Takes the gutter width from the bottom margin of .post

//	var gutter = parseInt(jQuery('.post').css('margin-bottom'));
	var container = $('#posts');



	// Creates an instance of Masonry on #posts

	container.masonry({
		gutter: '.gutter-sizer',
		itemSelector: '.post',
		columnWidth: '.column-sizer',
		percentPosition: true
	});


	function appendToMasonry(data){
	    $items = $(data)
	    container.append($items);
	    container.masonry('appended',$items);
	}
	function prependToMasonry(data){
	    $items = $(data)
	    container.prepend($items);
	    container.masonry('prepended',$items);
	}
	
	
	
	// This code fires every time a user resizes the screen and only affects .post elements
	// whose parent class isn't .container. Triggers resize first so nothing looks weird.
	
//	jQuery(window).bind('resize', function () {
//		if (!jQuery('#posts').parent().hasClass('container')) {
//
//
//
//			// Resets all widths to 'auto' to sterilize calculations
//
//			post_width = jQuery('.post').width() + gutter;
//			jQuery('#posts, body > #grid').css('width', 'auto');
//
//
//
//			// Calculates how many .post elements will actually fit per row. Could this code be cleaner?
//
//			posts_per_row = jQuery('#posts').innerWidth() / post_width;
//			floor_posts_width = (Math.floor(posts_per_row) * post_width) - gutter;
//			ceil_posts_width = (Math.ceil(posts_per_row) * post_width) - gutter;
//			posts_width = (ceil_posts_width > jQuery('#posts').innerWidth()) ? floor_posts_width : ceil_posts_width;
//			if (posts_width == jQuery('.post').width()) {
//				posts_width = '100%';
//			}
//
//
//
//			// Ensures that all top-level elements have equal width and stay centered
//
//			jQuery('#posts, #grid').css('width', posts_width);
//			jQuery('#grid').css({'margin': '0 auto'});
//
//
//
//		}
//	}).trigger('resize');



$(document).ready(function(){
    var video = $("#jquery_jplayer_1").data("video-url");
    $("#jquery_jplayer_1").jPlayer({
        ready: function(event) {
            $(this).jPlayer("setMedia", {
//				title: "Bubble",
				m4v: video,
            });
        },
        swfPath: "http://jplayer.org/latest/dist/jplayer",
        supplied: "m4v",
		wmode: "window",
		useStateClassSkin: true,
		autoBlur: false,
		smoothPlayBar: true,
		keyEnabled: true,
		remainingDuration: true,
		toggleDuration: true
    });



    $('.bootstrap-carousel').carousel({
//      interval:false // remove interval for manual sliding
    });

    // when the carousel slides, load the ajax content
    $('.bootstrap-carousel-lazy').on('slide.bs.carousel', function (e) {
        // get index of currently active item
        var item = $(e.target);

        var innerCarousel = item.find(".carousel-inner");
        var activeItem = item.find('.item.active').next();

        if(activeItem != undefined){
             carouselNormalization(item);
            //        var idx = activeItem.index();
            var url = activeItem.attr('data-next-page-url');
            if(url != undefined && url.trim() != ""){

                AjaxGet(url,
                  function(data){
                      jsonres = JSON.parse(data);

                      if(jsonres.Response.trim() != ""){
                        innerCarousel.append(jsonres.Response);
                      }
                        activeItem.removeAttr("data-next-page-url");
                         item.carousel({
//                          interval:false // remove interval for manual sliding
                        });
                });
            }
        }


//        // ajax load from data-urlal
//        $('.item').html("wait...");
//        $('.item').load(url,function(result){
//            $('.bootstrap-carousel-lazy').carousel(idx);
//        });

    });

//    // load first slide
//    $('[data-slide-number=0]').load($('[data-slide-number=0]').data('url'),function(result){
//        $('.bootstrap-carousel-lazy').carousel(0);
//    });


    $('.bootstrap-carousel-lazy').each(function(index,item){
        if(!$(item).hasClass("first-item-loaded")){
            var innerCarrousel = $(item).find(".carousel-inner");
            AjaxGet($(item).data("url-firstpage"),
            function(data){
                jsonres = JSON.parse(data)
                if(jsonres.Next_data_url.trim() != "") {
                    AjaxGet(jsonres.Next_data_url,function(data2){
                        jsonres2 = JSON.parse(data2)
                        innerCarrousel.append(jsonres2.Response);

                    });
                }

                innerCarrousel.append(jsonres.Response);
                $(item).addClass("first-item-loaded");
                innerCarrousel.find("[data-next-page-url]:first").removeAttr("data-next-page-url");
            });
        }
    });

    $(".lazy-load").each(function(index,item){
         AjaxGet($(item).data("url"),
            function(data){
                jsonres = JSON.parse(data)
                $(item).html(jsonres.Response)
            })
    });


//    var form = $("input.typeahead").data("search-url")
//    $("input.typeahead").typeahead({
//        onSelect: function(item) {
//            console.log(item);
//	    },
//        ajax: {
//            url: form,
//            timeout: 500,
//            displayField: "title",
//            triggerLength: 1,
//            method: "get",
//            loadingClass: "loading-circle",
//            preDispatch: function (query) {
//                showLoadingMask(true);
//                return {
//                    search: query
//                }
//            },
//            preProcess: function (data) {
//                showLoadingMask(false);
//                if (data.success === false) {
//                    // Hide the list, there was some error
//                    return false;
//                }
//                // We good!
//                return data.mylist;
//            }
//        }
//    });



        $(document).mouseup(function(e) {
            $(".hide-on-outside-click").each(function(index,item){
                // if the target of the click isn't the container nor a descendant of the container
                if (!$(item).is(e.target) && $(item).has(e.target).length === 0) {
                    $(item).remove();
                }
            });
        });
});

function NeglectArrowKeys(textbox,e){
			if (e.keyCode == 37) {
				// left
				e.preventDefault();
				return false;
			} else if (e.keyCode == 38) {
				// up
				e.preventDefault();
				return false;
			} else if (e.keyCode == 39) {
				// right
				e.preventDefault();
				return false;
			} else if (e.keyCode == 40) {
				// down
				e.preventDefault();
				return false;
			}  else if (e.keyCode == 16) {//Shift
				e.preventDefault();
				return false;
			} else if (e.keyCode == 17) {//ctrl
				e.preventDefault();
				return false;
			} else if (e.keyCode == 18) {//ctrl
				e.preventDefault();
				return false;
			}
			return true;

}

function EnterKeyPressed(textbox,e){
    if (e.keyCode == 13) {//Enter
        e.preventDefault();

        return true;
    }
}

function EscapeKeyPressed(textbox,e){
    if (e.keyCode == 27) {//Escape
        return true;
    }
}

function SuggestSearchItems(textbox,target,class,e){
    var url =  $(textbox).data("search-url") + "/" + $(textbox).val();

    if(EnterKeyPressed(textbox,e)){
        window.location = url;
    }

    if(NeglectArrowKeys(textbox,e) == false){
        return;
    }

//    e.preventDefault();
//    var blocksPerRow = 1;
    var searchResultBox = $("[data-text-box='"+$(textbox).attr("id")+"']");
    if(EscapeKeyPressed(textbox,e)){
        searchResultBox.remove();
        return;
    }

    if($(textbox).val().trim().length == 0){
        searchResultBox.remove();
    }



//    if(searchResultBox.length > 0) {
//        var thisIndex = $(".selected").index();
//        var newIndex = null;
//        var  arrowKeyPressed = false;
//        if(e.keyCode === 38) {
//
//            // up
//           newIndex = thisIndex - blocksPerRow;
//           arrowKeyPressed = true;
//        }
//        else if(e.keyCode === 40) {
//            // down
//            newIndex = thisIndex + blocksPerRow;
//            arrowKeyPressed = true;
//        }
//        if(newIndex !== null) {
//            $("a").eq(newIndex).addClass("selected").siblings().removeClass("selected");
//        }
//
//        if(arrowKeyPressed){
//            return;
//        }
//    }

    if($(textbox).val().length > 0){
        ShowSearchSuggestionBox(textbox,target,class);

        AjaxGet(url, function(data){
            var jsonres =  JSON.parse(data)
            searchResultBox.html(jsonres.Response);
        });
    }
}

function ShowSearchSuggestionBox(textbox,target,class){
    loadedSearchResult  = $("[data-text-box='"+$(textbox).attr("id")+"']");
    if(loadedSearchResult.length ==0){
        var html  = "<div class='search-suggestion-box hide-on-outside-click "+class+"' data-text-box='" +$(textbox).attr("id")+ "'><div class='loading-circle'></div></div>"
        if(target != undefined){

            $(target).append(html);
        }else{
            $(textbox).after(html);
        }
    }else{
        loadedSearchResult.append("<div class='loading-circle'></div>");
    }
}


function carouselNormalization(element) {
    var items = $(element).find('.item'), //grab all slides
    heights = [], //create empty array to store height values
    tallest; //create variable to make note of the tallest slide

    if (items.length) {
        function normalizeHeights() {
            items.each(function() { //add heights to array
                heights.push($(this).height());
            });
            tallest = Math.max.apply(null, heights); //cache largest value
            items.each(function() {
                $(this).css('min-height',tallest + 'px');
            });
        };
        normalizeHeights();

        $(window).on('resize orientationchange', function () {
            tallest = 0, heights.length = 0; //reset vars
            items.each(function() {
                $(this).css('min-height','0'); //reset min-height
            });
            normalizeHeights(); //run it again
        });
    }
}



function ResizeCarouselAccordingtoContent(element){


    var maxheight = 0
    $(element).find(".item").each(function(index,item){
        var itemHeight= $(item).height();

//console.log(itemHeight)
        if( itemHeight> maxheight){
            maxheight = itemHeight
        }

    });
    $(element).find(".carousel-inner").height(maxheight);
}

function AjaxGet(url, successCallback){
    $.ajax({
      url: url,
//      data: {
//         format: 'json'
//      },
      error: function(xhr, status, error, element) {
        console.log(xhr)
        ErrorDandler(xhr, status, error, element)
//         $('#info').html('<p>An error has occurred</p>');
      },
//      dataType: 'jsonp',
      success: function(data) {
         successCallback(data);
      },
      type: 'GET'
   });
}



function RedirectTo(data, element, toBlank) {
    if (data == '') {
        window.location.replace("/Account/Login");
    }
    else {
        if (toBlank) {
            window.open(
                data.url,
                '_blank' // <- This is what makes it open in a new window.
            );
        } else {
            window.location.replace(data.url);
        }
    }

};


function MessageAndRedirectTo(data, element, toBlank) {
    if (data.success) {
        ModalApear(data.message, "success");
        setTimeout(function() {
            RedirectTo(data, element, toBlank);
        }, 4000);
    }

}

function ErrorDandler(xhr, status, error, element) {
    if (xhr.status == 400) {
        var errors = JSON.parse(xhr.responseText).Errors;
        $(element).find("span[data-valmsg-for]").text("").removeClass("field-validation-error").addClass("field-validation-valid");
        $.each(errors, function (index, item) {
            $(element).find("span[data-valmsg-for='" + item.Key + "']").text(item.Message).removeClass("field-validation-valid").addClass("field-validation-error");
        });
    }
    //else if (xhr.status == 403) {
    //    window.location.replace("/Account/Login")
    //}
    else {
        var js = JSON.parse(xhr.responseText);
        Alert(js.message, "error");
    }
};

