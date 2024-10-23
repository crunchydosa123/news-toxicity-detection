import { createContext, useContext, useState } from "react";

const KeywordsContext = createContext();

export const KeywordsProvider = ({ children }) => {
    const [keywords, setKeywords] = useState();

    return (
        <KeywordsContext.Provider value={{ keywords, setKeywords }}>
            { children }
        </KeywordsContext.Provider>
    )
};

export default KeywordsContext;``