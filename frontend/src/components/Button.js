import React from 'react';
import '../styles.css';

const STYLES = ['btn--primary', 'btn--outline'];

const SIZES = ['btn--medium', 'btn--large', 'btn--mobile', 'btn--wide'];

const COLOR = ['primary', 'blue', 'red', 'green'];

const FUNCTION = ['imgUpload', 'audioUpload' ];
export const Button = ({
  children,
  type,
  clickHandler,
  buttonStyle,
  buttonSize,
  buttonColor,
  btnId
}) => {
  const checkButtonStyle = STYLES.includes(buttonStyle)
    ? buttonStyle
    : STYLES[0];

  const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize : SIZES[0];
  const checkButtonColor = COLOR.includes(buttonColor) ? buttonColor : null;
  const checkbtnId = FUNCTION.includes(btnId) ? btnId : null;
  
  // function clickHandler(){
  //   console.log({btnId});
  //   // === 'audioUpload') ? alert('Audio') : null;
  // }

  return (
    <button
      className={`btn ${checkButtonStyle} ${checkButtonSize} ${checkButtonColor}`}
      onClick={clickHandler}
      type={type}
      id={`${checkbtnId}`}
    >
      {children}
    </button>
  );
};

