import React, { Component } from 'react'
import { Button } from './Button'

class ClassClick extends Component {

  clickHandler(){
    console.log("clickHandler click")
  }
  render() {
    return (
      <div>
        <Button onClick={this.clickHandler} buttonSize='btn--wide' buttonColor='blue'>진단하기 2 </Button>
      </div>
    )
  }
}

export default ClassClick

function FunctionClick(){
  function clickHandler () {
    console.log('clickhandler click')
  }
  return (
    <div>
      <Button onClick={this.clickHandler} buttonSize='btn--wide' buttonColor='blue'>진단하기 2 </Button>
    </div>
  )
}