import React, {useState} from 'react'
import '../../css/info.css'
import MyStocks from './myStocks'
import MyTriggers from './myTriggers'


function DisplayContainer(props) {

    const [selected, setSelected] = useState("mystocks")

    var stockList = null

    return (
        <div className="displayContainer">
            <div className="optionsContainer">
                <div className={selected=="mystocks" ? "selectedOption" : "option"} onClick={()=>setSelected("mystocks")}>
                    My Stocks
                </div>
                <div className={selected=="mytriggers" ? "selectedOption" : "option"} onClick={()=>setSelected("mytriggers")}>
                    My Triggers
                </div>
            </div>
            <div className="contentDisplay">
                {selected=="mystocks" ? 
                (<div>
                    <div className="contentTitle">My Stocks</div>
                    <MyStocks user={props.user} info={props.info} setInfo={props.setInfo}/>
                 </div>
                )
                : selected=="mytriggers" ?
                (<div>
                    <div className="contentTitle">My Triggers</div>
                    <MyTriggers user={props.user} info={props.info} setInfo={props.setInfo}/>
                </div>)
                : 
                (
		<div>
			<div className="contentTitle">My History</div>
		</div>)
            }
            </div>
            {/* depending on what is selected, display different info here */}
        </div>
    )
}

export default DisplayContainer
