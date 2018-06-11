import {Injectable} from '@angular/core';

import {HttpClient, HttpHeaders} from '@angular/common/http';
import {browser} from 'protractor';

@Injectable()
export class SearchingService {

  constructor(private http: HttpClient) {
  }

  aim = {
    what: '',
    whichPage: 0,
    howMuchPerPage: 20,
    browserType: 'tor',
    actualBrowserType: 'tor',
    enterFromPrevious: ""
  };

  count;
  results1 = [];
  results2 = [];
  lastPage;
  pagination;

  search(what, whichPage = 0, howMuchPerPage = this.aim.howMuchPerPage, browserType = this.aim.browserType) {
    this.aim.whichPage = whichPage;
    this.aim.howMuchPerPage = howMuchPerPage;
    this.aim.browserType = browserType;
    if (this.aim.what !== what || this.aim.actualBrowserType !== this.aim.browserType) {
      console.log(this.aim.whichPage);
      this.http.get('http://localhost:9112/api/' + this.aim.browserType + '/count?key=' + what)
        .subscribe(
          (response) => {
            this.count = response[0].count;
            console.log(this.count);
            this.changePagination();
          },
          (error) => console.log(error)
        );
    }
    console.log(this.aim.actualBrowserType);
    console.log(this.aim.browserType);
    this.aim.actualBrowserType = this.aim.browserType;
    this.aim.what = what;
    this.http.get('http://127.0.0.1:9112/api/' + this.aim.browserType + '/search?key=' + what + '&ppage=' +
      howMuchPerPage + '&page=' + whichPage)
      .subscribe(
        (response) => {
          console.log(response);
          const results = Object.values(response);
          for(let i=0; i<results.length; i++) {
            if(i%2==0)
              this.results2.push(results[i]);
            else
              this.results1.push(results[i]);
          }
          this.changePagination();
          if(this.aim.actualBrowserType == "iot")
            this.setFlags();
        },
        (error) => console.log(error)
      );
  }

  setFlags() {
    for (let i = 0; i < this.results2.length; i++) {
      this.http.get('http://freegeoip.net/json/'+this.results2[i].ip).subscribe(
        (response) => {
          console.log(response);
          this.results2[i].countryCode = response['country_code'];
          console.log(response);
        },
        (error) => console.log(error)
      );
      this.http.get('http://freegeoip.net/json/'+this.results1[i].ip).subscribe(
        (response) => {
          console.log(response);
          this.results1[i].countryCode = response['country_code'];
        },
        (error) => console.log(error)
      );
    }
  }

  changePagination() {
    this.lastPage = Math.floor(this.count / this.aim.howMuchPerPage);
    console.log(this.lastPage);
    this.pagination = [this.aim.whichPage];

    let pagesInPagination = 0;
    for (let i = 1; i < 10; i++) {
      if ((this.aim.whichPage + i) <= this.lastPage) {
        this.pagination.push(this.aim.whichPage + i);
        pagesInPagination++;
      }
      if ((this.aim.whichPage - i) >= 0) {
        this.pagination.push(this.aim.whichPage - i);
        pagesInPagination++;
      }
      if (pagesInPagination > 10) {
        break;
      }
    }
    this.pagination.sort(function (a, b) {
      return a - b;
    });
  }

  setResultsPerPage(perPage: number) {
    this.aim.howMuchPerPage = perPage;
  }

  setBrowserType(browserType: string) {
    console.log('ustawiam browser type na: ' + browserType);
    this.aim.browserType = browserType;
  }

  getSettings() {
    return this.aim;
  }


}
