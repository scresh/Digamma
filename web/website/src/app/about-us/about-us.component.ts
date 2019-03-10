import { Component, OnInit } from '@angular/core';

import { we } from './information-about-us';

@Component({
  selector: 'app-about-us',
  templateUrl: './about-us.component.html',
  styleUrls: ['./about-us.component.css']
})
export class AboutUsComponent implements OnInit {

  constructor() { }

  we;

  ngOnInit() {
    this.we = we;
  }

}
