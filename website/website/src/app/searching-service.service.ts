import {Injectable} from '@angular/core';

import {HttpClient, HttpHeaders} from '@angular/common/http';

@Injectable()
export class SearchingService {

  constructor(private http: HttpClient) {
  }

  aim = {
    what: "",
    whichPage: 0,
    howMuchPerPage: 40
  };

  count;
  results1;
  results2;
  lastPage;
  pagination;

  search(what, whichPage = 0, howMuchPerPage = 40) {
    this.aim.whichPage = whichPage;
    this.aim.howMuchPerPage = howMuchPerPage;
    if (this.aim.what != what) {
      console.log("1");
      this.http.get("http://localhost:9112/api/count?key=" + what)
        .subscribe(
        (response) =>  {this.count = response[0].count;
          console.log(this.count);},
        (error) => console.log(error)
    );
    }
    this.aim.what = what;
    this.http.get("http://127.0.0.1:9112/api/search?key=" + what + "&ppage=" + howMuchPerPage + "&page=" + whichPage)
      .subscribe(
        (response) => {
          console.log(response);
          let half = this.aim.howMuchPerPage/2;
          let results = Object.values(response);
          this.results2 = results.slice(0,results.length/2);
          this.results1 = results.slice(results.length/2,results.length);
          this.changePagination()},
        (error) => console.log(error)
      );

  }

  changePagination() {
    this.lastPage = Math.floor(this.count/this.aim.howMuchPerPage);
    console.log(this.lastPage);
    this.pagination = [this.aim.whichPage];

    var pagesInPagination = 0;
    for(let i=1; i<10; i++){
      if((this.aim.whichPage+i)<=this.lastPage) {
        this.pagination.push(this.aim.whichPage + i);
        pagesInPagination++;
      }
      if((this.aim.whichPage-i)>=0) {
        this.pagination.push(this.aim.whichPage - i);
        pagesInPagination++;
      }
      if(pagesInPagination>10)
        break;
    }
    this.pagination.sort(function(a, b){return a-b});
  }

}
