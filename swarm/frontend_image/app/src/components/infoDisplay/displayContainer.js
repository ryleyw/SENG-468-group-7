import React, {useState} from 'react'
import '../../css/info.css'

function DisplayContainer(props) {

    const [selected, setSelected] = useState("mystocks")

    var stockList = null

    // if (props.info != null && props.info.stocks!=undefined) {

    // }
    // stockList = props.info.stocks.entries().map((stock))
    //     <div className="stockEntry" key={i}>

    //     </div>
    // )

    //from info, load my triggers, my stocks
    //at top of my stocks / top of my triggers, have buy stock / set trigger

    //each entry in a stock should be able to sell a certain amount of a stock, or cancel a trigger

    //click buy stock -> look up stock -> get quote price -> enter amount to buy -> issue command -> commit buy

    //click sell stock -> get quote price -> enter amoutn to sell -> issue comand -> commit sell

    //click set trigger -> same as buy stock, but set price point / choose from existing stocks


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
                (<div className="contentTitle">My Stocks</div>)
                : selected=="mytriggers" ?
                (<div className="contentTitle">My Triggers</div>)
                : 
                (<div className="contentTitle">Other</div>)
            }
            </div>
            {/* depending on what is selected, display different info here */}
        </div>
    )
}

export default DisplayContainer