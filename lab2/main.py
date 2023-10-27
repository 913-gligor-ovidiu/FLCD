from SymbolTable import SymbolTable

if __name__ == "__main__":
    st = SymbolTable(5)
    st.insert(0)
    st.insert(1)
    st.insert("x")
    st.insert("y")
    st.insert("z")
    st.insert(12)
    st.insert("13")

    assert st.get("x") == 3
    assert st.get("y") == 4
    assert st.get("z") == 5
    assert st.get(12) == 6
    assert st.get("13") == 7
    assert st.get("a") == None

    st.display()