import { Component, OnInit } from '@angular/core';
import {Router} from "@angular/router";
import { PlatformLocation } from '@angular/common'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  query= '';
  searchType = 'tor';
  message ='Enter query:';

  search(){
    let words = this.query.split(" ").filter(function (x) {return x != '';});

    if (words.length > 12){
      this.message = 'Too many words';

    } else if(words.length < 1){
      this.message = 'Enter at least one word';

    } else {

      for (let word of words) {
          if (word.length > 16 || word.length < 1){
            this.message = 'Word length too long';
            return;
          }
      }
      this.router.navigate(['/results/' + this.searchType + '/' + this.query]);
    }
  }

  constructor(private router: Router, private platformLocation: PlatformLocation) { }

  ngOnInit() {
    this.platformLocation.onPopState(() => {
      location.reload();
    });
  }

  setTor(){
    this.searchType = 'tor';
  }

  setIoT(){
    this.searchType = 'iot';
  }


}

